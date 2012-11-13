#!/usr/bin/perl
use X11::GUITest qw/StartApp WaitWindowViewable SendKeys/;

StartApp('firefox');

# Wait for application window to come up and become viewable. 
my ($GEditWinId) = WaitWindowViewable('firefox');
if (!$GEditWinId) {
    die("Couldn't find gedit window in time!");
}

SendKeys('{F11}');

