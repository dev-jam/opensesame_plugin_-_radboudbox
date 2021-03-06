OpenSesame Plug-in: Radboud Buttonbox 'Wait Buttons' plugin
==========

*An OpenSesame Plug-in for collecting button responses, audio detection, voice key and sending stimulus synchronization triggers with the Radboud Buttonbox to data acquisition systems.*  

Copyright, 2021, Bob Rosbag  

This plugin makes use of the RuSocSci python package developed by Wilbert van der Ham. Radboud Buttonbox is developed by Pascal de Water. Exact references will follow in the future. 


## 1. About
--------

The 'Wait Buttons' can be used for time accurate(1ms) button press/release, audio detection and voice key.
Upper case A, B, C, D, E, F are used for key presses, and lower case a, b, c, d, e, f are used for key releases. Uppercase S is used for sound key detection and uppercase V for voice key.  

**Note:** this is a foreground item, it will wait for the button press/release or till the timeout has ended before advancing to the next item.

This item has two parameters:

- *Allowed Responses* list of buttons separated by ';'
- *Timeout* time to wait for a button press/release


For more information:

<http://tsgdoc.socsci.ru.nl/index.php?title=ButtonBoxes>



## 2. LICENSE
----------

The Radboud Buttonbox plug-in is distributed under the terms of the GNU General Public License 3.
The full license should be included in the file COPYING, or can be obtained from

- <http://www.gnu.org/licenses/gpl.txt>

This plug-in contains works of others.


## 3. Documentation
----------------

Installation instructions and documentation on OpenSesame are available on the documentation website:

- <http://osdoc.cogsci.nl/>
