---
layout: post
title: "Accessing a firewalled computer/Raspberry Pi with Wireguard and OpenWRT, the easy way"
---

Suppose you have a computer or Raspberry Pi named Alice behind a school/corp firewall. You have a router running OpenWRT called Bob at home you can open ports. You wish to to access remotely from home.
Suppose you're a n00b in networking and routing stuff and too lazy to learn it properly like me. You know how superficially how a router and subnetting works. You know how to set up your home network so each computer has an IP, you can probably do some port forwarding and Dynamic DNS, but don't know exactly what the heck all the routing lingos mean.

I have a computer behind a campus firewall that I want to connect to from my home. 
I can always VPN in, but I don't like having to open the VPN client and figure out how to not route all my traffic through the campus VPN.
Normally, I do the [reverse-SSH/autossh](https://blog.devolutions.net/2017/3/what-is-reverse-ssh-port-forwarding) kinda thing to reverse-open a port on the home router. 
However, there are two shortcomings with reverse-SSH. 
First, it doesn't route UDP and I have to be explicit about ports I want to forward. 
Second, it's a pain to set up. 
Services such as [r3mot3.it makes it zero-configuration](https://www.remot3.it/web/index.html), but it's a proxying service so it's slow.

You need to use Wireguard like me. Wireguard solves all of those elegantly and it's very performant. Plus it's integrated with systemd so you have easy startup configure. [It's really quite magical and just works](https://lwn.net/Articles/748582/). 

So, let's get down to getting Wireguard to work.

**Installing Wireguard on router Bob**

Get OpenWRT latest stable version (don't get the dev version) - currently it's still named LEDE now, it hasn't released a version after the name change to OpenWRT. Install `luci-app-wireguard` and `luci-proto-wireguard`.

**Installing Wireguard on computer Alice**

On Alice, install Wireguard [by whatever mean that you need to](https://www.wireguard.com/install/). On most Linux system it's just a couple of commands just like the page says.

If Alice is a Raspberry Pi, then do the following:

1. Go to [The Wireguard Install page](https://www.wireguard.com/install/), then look at the section Debian (module, tools).
2. Click on the Module link. Download the "all" arch package to the
Pi. Install `dkms` and `raspberrypi-kernel-headers`. Then `dpkg -i` the
`wireguard-dkms` deb file you just downloaded.
3. Click on the Tools link. Download the "armel" arch package to the
Pi (armel, not armhf - the Raspberry Pi's CPU doesn't have some of the
features of the armhf arch in Debian, if you download and install the armhf package, it will crash).

Now we have to make a "fake" armhf package from the armel package. It's just
userland tools, it doesn't matter if they are a bit less performant.

```bash
$ mkdir wireguard-tools-repack

$ cd wireguard-tools-repack

$ ar x ../wireguard-tools_blah_armel.deb

$ vim control.tar.xz # Yeah you see it correctly :) 

Edit the control file so it says: 
Architecture: armhf
instead of 
Architecture: armel

$ ar r ../wireguard-tools_blah_armel.deb control.tar.xz
```

Then `dpkg -i` the repacked file. Now dpkg won't complain no more.

**Generate key pairs**

Now generate two keypairs for the computer and the router. Do it on the computer Alice.

```bash
$ wg keygen | tee alice_key.priv | wg pubkey | tee alice_key.pub
$ wg keygen | tee bob_key.priv | wg pubkey | tee bob_key.pub
```

Note that from now when I say `alice_key.priv`, it *always* means pasting whatever that is in `alice_key.priv`, not the filename.

**Configure router Bob**

Go to the router's Luci interface:

1. Network -> Interfaces -> Add new interfaces -> Protocol -> WireGuard VPN, name it `wg0`. Next.
2. "General Setup" tab: Common Configuration -> Private key:
`bob_key.priv`. Listen Port `4500` (like Cisco Anyconnect). IP Addresses: `192.168.2.1/24` (not
your LAN subnet).
3. Peers -> Pubkey -> Pub key: `alice_key.pub`. Allowed IPs: `192.168.2.2/32`
-- and whatever IPs you want to access pass through Alice (as if Alice
was your VPN provider. For example, like something else inside its firewalled
network.
4. "Firewall Settings" tab: Assign firewall-zone: `WAN`.
5. Remember to port-forward port `4500/UDP` on Bob to the router itself.

Done for the router. Restart it. Watch what it does on Status > Wireguard.

**Configure the computer Alice**

```bash
$ sudo vim /etc/wireguard/wg0.conf
```

Type in:

```ini
[Interface]
Address = 192.168.2.2/24
ListenPort = 58601
PrivateKey = alice_key.priv

[Peer]
PublicKey = bob_key.pub
AllowedIPs = 192.168.2.1/32
Endpoint = your-bob-router.dyndns.org:4500
PersistentKeepalive = 25
```

Try it:

```bash
$ wg-quick up wg0
```

See if it works:

```bash
$ sudo wg
```

If you're happy:

```bash
$ wg-quick down wg0

$ sudo systemctl enable wg-quick@wg0
```

Now your computer Alice, it will appear as if it's not firewalled on `192.168.2.2`. 
You can add as many peers as you want on the router's peers section. 
Just repeat the steps on the Alice computer and give it a new IP. 
All of the wireguard peers can share the same `wg0` interface on the router.

Isn't that sweet?
