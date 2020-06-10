# GOES-16 Desktop Wallpaper Updater

A single Python script which updates a Windows desktop wallpaper to the most recent image of the US from the GOES-16 satellite. 

## TODO

Since I wrote this script, NOAA has made the GOES data more readily available. Most of this code is unnecessary now that a 5000x3000 JPG is available directly from NOAA at https://cdn.star.nesdis.noaa.gov/GOES16/ABI/CONUS/GEOCOLOR/latest.jpg

## Running Periodically

To run periodically, I have a task setup in Windows Task Scheduler with the following settings:
 * Trigger:
   * One-time trigger starting whenever you're setting it up.
   * After triggered, repeat every X minutes/hours indefinitely. (I currently use 1 hour. There's an updated image for CONUS every 5 minutes.)
 * Action: Start a program with pythonw.exe and goes\_wallpaper.pyw.
 * Condition: Start only if a network connection is available.
 * Settings: 
   * Run task as soon as possible after a scheduled start is missed. 
   * If the task is already running, then do not start a new instance.
   * Run only when user is logged on.

There's probably a better way, but it works.

## License

Copyright Paul Harris. Please ask before sharing as I don't want to overwhelm the Colorado State server with requests. I've tried to make it as easy on the server as possible, but still.
