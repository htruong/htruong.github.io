---
layout : "post"
title : "Linear Edit Distance/Needleman-Wunsch calculation in Javascript"
---

The project I am working on requires me to make a function to calculate edit distance between two arbitrary sentences. I just happen to have a very good understand on this topic and hereby write a function to do just that, in linear memory requirement, in other words [Hirschberg's algorithm](https://en.wikipedia.org/wiki/Hirschberg's_algorithm). I actually have a much beefier  implementation with a lot of clever tricks of the same problem in CUDA, which was [published last year](http://link.springer.com/article/10.1007/s11265-014-0883-2). 

You can adapt, edit, improve, whatever you want to do with this code. I would appreciate it if you could credit me, but that's optional. I know you could just have come up with this yourself, but why waste time duplicating efforts?


```javascript
// Needleman-Wunsch linear alignment of two arrays
// WTFPL license
// 2015 Huan Truong - htruong@tnhh.net
function align(a, b) {
    var current = [];
    var lookback = [];

    var nw_match = 2;
    var nw_mismatch = -1;
    var nw_indel = -1;

    for (var j = 0; j < b.length + 1; j++) {
        current[j] = j * nw_indel;
    }

    for (var i = 1; i < a.length + 1; i++) {
        for (var j = 0; j < b.length + 1; j++) {
            lookback[j] = current[j];
        }
        current[0] = i * nw_indel;
        for (var j = 1; j < b.length + 1; j++) {
            if (a[i-1] === b[j-1]) {
                current[j] = lookback[j-1] + nw_match;
            } else {
                current[j] = Math.max(lookback[j-1] + nw_mismatch,
                                Math.max(lookback[j] + nw_indel,
                                    current[j-1] + nw_indel));
            }
        }
    }

    return current[b.length];
}
```

