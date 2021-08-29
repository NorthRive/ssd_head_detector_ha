===========================
VGG HOLLYWOOD HEADS Dataset
===========================

This package contains a set of images extracted from Hollywood movies where people have been annotated at both head and upperbody-level.

It has been used to train the head detector used in [1] and [2].

How to use the helper code:
===========================
Within a Matlab session, type:

annotfile = 'upperbody.annotation';
imagespath = './keyframes';
scalename = '';
anglename = '';
verbose = 1;

samples = loadAnnotatedHeads(annotfile, scalename, anglename, imagespath, verbose);


References
==========
[1] M. Marin-Jimenez, A. Zisserman, V. Ferrari
"Here's looking at you, kid." Detecting people looking at each other in videos
Proceedings of the British Machine Vision Conference, 2011 
[2]  M. Marin-Jimenez, A. Zisserman, M. Eichner, V. Ferrari
Detecting People Looking at Each Other in Videos  
International Journal of Computer Vision, Volume 106, Number 3, page 282--296, feb 2014 