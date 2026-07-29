# Elite Universe Editor on the Commodore 64

![The Elite Universe Editor on the Commodore 64](https://elite.bbcelite.com/images/github/elite-universe-editor-home-screen-c64.png)

This repository contains source code for the Elite Universe Editor on the Commodore 64. You can build it using `./build.sh`.

The Elite Universe Editor allows you to create your own universes in classic BBC Micro and Commodore 64 Elite. For more information, see the [bbcelite.com website](https://elite.bbcelite.com/hacks/elite_universe_editor.html).

This repository contains the Universe Editor code as a submodule:

* [Elite Universe Editor library](https://github.com/markmoxon/elite-universe-editor-library)

This code is patched into Elite. You can search the source code for the patch points by searching the sources for `Mod:`.

The following repositories are used to generate the Universe Editor for the different platforms:

* [BBC Master Elite Universe Editor](https://github.com/markmoxon/elite-universe-editor-bbc-master)
* [6502 Second Processor Elite Universe Editor](https://github.com/markmoxon/elite-universe-editor-6502-second-processor)
* [Commodore 64 Elite Universe Editor](https://github.com/markmoxon/elite-universe-editor-commodore-64)

The above repositories are used when building the Universe Editor and the Elite Compendium discs:

* [Elite Universe Editor](https://github.com/markmoxon/elite-universe-editor)
* [Elite Compendium (BBC Master)](https://github.com/markmoxon/elite-compendium-bbc-master)
* [Elite Compendium (BBC Micro)](https://github.com/markmoxon/elite-compendium-bbc-micro)

In all cases, child code is included in a parent using a submodule.

## Acknowledgements

Commodore 64 Elite was written by Ian Bell and David Braben and published by Firebird, and is copyright &copy; D. Braben and I. Bell 1985.

The Commodore 64 game disks in this repository are very similar to those released on [Ian Bell's personal website](http://www.elitehomepage.org/), but to ensure accuracy to the released versions, I've used disk images from the [Commodore 64 Preservation Project](https://archive.org/details/C64_Preservation_Project_10th_Anniversary_Collection) (it turns out that the disk images on Ian Bell's site differ slightly from the official versions). The Commodore Plus/4 version is based on the disk image from Ian Bell's site.

The commentary is copyright &copy; Mark Moxon. Any misunderstandings or mistakes in the documentation are entirely my fault.

Huge thanks are due to the original authors for not only creating such an important piece of my childhood, but also for releasing the source code for us to play with. Also, a big thumbs up to Kroc Camen for his epic [Elite Harmless](https://github.com/Kroc/elite-harmless) project, which is a really useful reference for anyone exploring the C64 binaries. Finally, thanks to the gurus in this [Lemon64 forum thread](https://www.lemon64.com/forum/viewtopic.php?t=67762&start=90) for their sage advice.

### A note on licences, copyright etc.

This repository is _not_ provided with a licence, and there is intentionally no `LICENSE` file provided.

According to [GitHub's licensing documentation](https://docs.github.com/en/free-pro-team@latest/github/creating-cloning-and-archiving-repositories/licensing-a-repository), this means that "the default copyright laws apply, meaning that you retain all rights to your source code and no one may reproduce, distribute, or create derivative works from your work".

The reason for this is that the Universe Editor is intertwined with the original source code for Elite, and the original source code is copyright. The whole site is therefore covered by default copyright law, to ensure that this copyright is respected.

Under GitHub's rules, you have the right to read and fork this repository... but that's it. No other use is permitted, I'm afraid.

My hope is that the educational and non-profit intentions of this repository will enable it to stay hosted and available, but the original copyright holders do have the right to ask for it to be taken down, in which case I will comply without hesitation. I do hope, though, that along with the various other disassemblies and commentaries of this source, it will remain viable.

---

Right on, Commanders!

_Mark Moxon_