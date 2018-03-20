---
layout: post
title: "Accessing a firewalled Computer or Raspberry Pi remotely with Wireguard and OpenWRT the easy way"
---

Suppose you have a computer or Raspberry Pi named Alice behind a school/corp firewall you wish to to access remotely from home. You have a router running OpenWRT called Bob at home you can open ports. You want to have an automated/easy way to access it.

If you're not happy with the current firewall/VPN affair, use Wireguard. 
[It's really quite magical](https://lwn.net/Articles/748582/). 
I have a computer behind a campus firewall that I want to connect to from my home. 
I can always VPN in, but I don't like having to open the VPN client and figure out route all my traffic through the campus VPN.
Normally, I do the reverse-SSH/autossh kinda thing to reverse-open a port on the home router. 
However, there are two shortcomings with reverse-SSH. 
First, it doesn't route UDP and I have to be explicit about ports I want to forward. 
Second, it's a pain to set up. 

Wireguard solves all of those elegantly and it's very performant.

Plus it's integrated with systemd so you have easy startup configure. Wireguard really just works.

So, let's get down to getting Wireguard to work.

**Installing Wireguard the easy way**

Get OpenWRT latest stable version (don't get the dev version) - currently it's still named LEDE now, that's before the name change. Install `luci-app-wireguard` and `luci-proto-wireguard`.

On Alice, install Wireguard [by whatever mean that you need to](https://www.wireguard.com/install/).

**If Alice was a Raspberry Pi**

1. Go to [The Wireguard Install page](https://www.wireguard.com/install/), then look at the section Debian (module, tools).
2. Click on the Module link. Download the "all" arch package to the
Pi. Install `dkms` and `raspberrypi-kernel-headers`. Then `dpkg -i` the
`wireguard-dkms` deb file you just downloaded.
3. Click on the Tools link. Download the "armel" arch package to the
Pi (armel, not armhf - the Raspberry Pi's CPU doesn't have some of the
features of the armhf arch in Debian, if you download and install the armhf package, it will crash).

Now we have to make a "fake" armhf package from the armel package. It's just
userland tools, it doesn't matter if it's less performant.

```
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

Now generate two keypairs for the computer and the router:

```
$ wg keygen | tee alice_key.priv | wg pubkey | tee alice_key.pub
$ wg keygen | tee bob_key.priv | wg pubkey | tee bob_key.pub
```

Note that when I say `alice_key.priv`, it just means paste whatever that is in `alice_key.priv`, not the filename.

**Configure the router Bob**

Go to the router's Luci interface:

1. Network>Interfaces>Add new interfaces>Protocol>WireGuardVPN, name `wg0`. Next.
2. "General Setup" tab: Common Configuration -> Private key:
bob_key.priv. Listen Port 4500. IP Addresses: 192.168.2.1/24 (not
your LAN subnet).
3. Peers -> Pubkey -> Pub key: alice_key.pub. Allowed IPs: 192.168.2.2/32
and whatever IPs you want to access pass through computer X (as if X
was your VPN provider) -- like something inside its firewalled
network.
4. "Firewall Settings" tab: Assign firewall-zone: WAN.

Done for the router. Restart it. Watch what it does on Status > Wireguard.

**Configure the computer Alice**

`$ sudo vim /etc/wireguard/wg0.conf`

Type in:

```
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

`$ wg-quick up wg0`

See if it works:

`$ sudo wg`

If you're happy:

```
$ wg-quick down wg0

$ sudo systemctl enable wg-quick@wg0
```

Now your computer Alice, it will appear as if it's not firewalled as 192.168.2.2. 
You can add as many peers as you want on the router's peers section. 
Just repeat the steps on the Alice computer and give it a new IP.

Isn't that sweet?
