# Ever wanted to boobytrap your own front door? Better yet, have you ever wanted the Seinfeld theme song to play every time you walk inside, like you're living in your very own sitcom? If so, you're in luck! If not, there is still hope

## Check out the main project [blog post on MakerShare](https://makershare.com/projects/seinfeld-boobytrap-hello-rich)

A tale of two buddies, and a third buddy who deserved more credit on this project

Once upon a time, a buddy (me) wanted to work more with embedded systems, so he asked another buddy (Rich) for ideas. Here is what other buddy said:

![Slide00](https://github.com/asa55/HelloRich/blob/master/slides/Slide00.png)

I realized this probably wouldn't fill the void in my heart to work on embedded systems, the likes of which I 'd rather run using C++ bare-metal, but it did spark my interest.

![Slide01](https://github.com/asa55/HelloRich/blob/master/slides/Slide01.png)

My first thought was that if we're going to build something reliable that's wireless, we'll need something battery powered. That said, we don't want something that will drain the battery in a day. Also, if we built a custom wireless Tx/Rx system, we were at a high risk of false positives. This quickly became not as easy, but thanks to other smart people, there just had to be an existing solution we could base our project off of.

![Slide02](https://github.com/asa55/HelloRich/blob/master/slides/Slide02.png)

I really wanted to use one of the main hobby electronics suppliers like sparkafruit or adafun, but the allure of 2 day shipping direct from Jeff Bezos was too great. It was vastly overkill. Somebody else already made a cheap and reliable door chime with a magnetic sensor that would ding every time you opened your door, and offered 52 pre-existing chimes (and obviously was less prone to battery draining and false-positives in the wee hours of the morning). Wow it would have been great if I could just overwrite their sounds with my own, but I didn't expect I'd be able to do that. So we went with the Parasyte (The Maxim) method and aimed to take over the brain of the chime with a Raspberry Pi. We opted for the Zero W model so that we could program it headless over WiFi and connect to an arbitrary Bluetooth speaker in case he really wanted to crank up the jamz in the future by connecting it to a more powerful speaker.

![Slide03](https://github.com/asa55/HelloRich/blob/master/slides/Slide03.png)

![Slide04](https://github.com/asa55/HelloRich/blob/master/slides/Slide04.png)

The complete Bill of Materials (a.k.a. all the stuf we bought for this project or happened to have laying around) is all stuff you can find on Amazon, and is mostly swappable for similar components.

* Any cheap wireless door chime that has a magnetic sensor and will light up when you open the door. (needs to light up because we use a photoresistor to detect the door opening). We used the Fosmon WaveLink Door Open Chime, but literally any door chime you're willing to mutilate should do the trick. The chime was in the range of $15 when I bought it a few days ago but they're already over $20 now for some reason. So just get whatever you can find that fits the project budget

* The Raspberry Pi Zero W. I said W H in the slide but that's not necessary - you'll need to solder some stuff anyways so soldering on your own header pins (hence the H) is not a big deal. I used the Vilros Raspberry Pi Zero W Basic Starter Kit, which comes with the knick knacks you need to get a Pi working if you've never done it before. The kit was less than $30

* Any cheap wireless bluetooth speaker. I used a 4COVR speaker that was like $10

* I had some basic tools laying around for electronics work - small screwdrivers, a cheap multimeter from radioshack from back when that was a thing, some soldering equipment, a drill with a small drill bit (then a slightly larger drill bit after I broke the first one), some electrical tape, some wire cutters, and some spare wires.

* You don't need a laptop with PuTTy, but if you want to safely shut the Pi down without plugging in a monitor/mouse/keyboard down the line you'll need any software that will let you SSH into the Pi

* The most important two pieces I haven't mentioned yet are trimpots and photoresistors. You should be able to get packs of assorted potentiometers and photoresistors on Amazon. It doesn't much matter which ones you get becasue the trimpot is used to compensate for the sensitivity (or lack thereof) of your photoresistor. The photoresistor I used was about 10k ohms in normal lighting conditions and 2k ohms when I flashed the chime's light on it, while the potentiometer (a.k.a. trimpot in this case) spanned 0 to 10k ohms, set at about 5k ohms. I'll detail the electronics better in a sec.

![Slide05](https://github.com/asa55/HelloRich/blob/master/slides/Slide05.png)

So we went about building the thing. We had lots of bad ideas along the way, so I'll only discuss the final build to avoid confusing myself any further.

The work is broken down into the electrical portion of the work and the software portion of the work.
On the electrical side:

![Slide06](https://github.com/asa55/HelloRich/blob/master/slides/Slide06.png)

OK so I wasn't very specific as to how to connect this-to-that, but that's OK because the only things that matter for this part are that (1) you can use electrical tape to tape the photoresistor directly to the face of any LED (2) the wires have enough length to run out the side of any hle you drill in your chime to get to the GPIO pins of your Raspberry Pi (implying you've already soldered header pins onto your Pi - I used female connectors so that I could plug the wires into the Pi directly). I mentioned you could use any photoresistors you want but if you don't have any laying around get a variety pack from Amazon and use the largest ones they give you (for example, TrustYiwen assorted photoresistor kit), in addition to a 10k trimpot or anything that the max resistance of the trimpot approximately equals the resistance of your photoresistor in ambient lighting (not pointed at a light, but not intentionally covered - you can measure this with your multimeter). I personally love the kit I have from IC Touch - not sure if it's still available on Amazon sinc I got it a year or two ago but it's a hundred or so assorted pots that can plug into a breadboard, the kind that you need a tiny flathead screwdriver to adjust. Any kit will do, of course.

![Slide07](https://github.com/asa55/HelloRich/blob/master/slides/Slide07.png)

So we built this voltage divider that relies on a few facts about the Pi... (1) the GPIO pin threshold between a logical 0 and a logical 1 is at about 1.2 volts. Also, the GPIO pins might break if you feed them more than 3.3V (a.k.a. 3V3). So we don't actually need the voltage present at the GPIO input to *be* 3V3 or 0V, we just need to cross the threshold. The way this is hooked up, we connected the photoresistor to the RasPi ground reference pin, so when the photodiode has a small resistance value compared to that of the potentiometer (about a third of the resistance), the voltage seen by the GPIO input will be less than the threshold voltage, and the Pi will interpret this as a logical 0. When the LED is not lit up, and the photoresistor has a relatively high value (about half of that of the potentiometer or more) we're safely above the threshold voltage and the RasPi will interpret this as a logical 1.

If you're wondering why I picked the pin range I did, well it's because of this:

![Slide08](https://github.com/asa55/HelloRich/blob/master/slides/Slide08.png)

We totally should have taken him up on that - my toddler-like attention span led us to this:

![Slide09](https://github.com/asa55/HelloRich/blob/master/slides/Slide09.png)

On the software side:

* In the Raspberry Pi kit you got an SD card - my laptop has an SD card writer build in (just some old HP laptop - nothing special) . If your PC doesn't have this you can buy an SD card writer on Amazon (like the Anker for less than $10).

* Download SDFormatter

* Download balenaEtcher

Use the SDFormatter software to wipe your SD card clean. Totally nuke everything inside (our SD card came with NOOB pre-installed but it didn't work properly, and this method is faster). Download the latest version of Raspbian from the Raspberry Pi website. We used 2019-09-26-raspbian-buster.img  for this project, but the rest of the software is somewhat invariant to the exact version of Raspbian, so it shouldn't need to be exact.

Use balenaEtcher to flash the Raspbian .img to your SD card.

Now I won't get into the details about how to turn on a Pi, but at this point you just slide the SD card into the Pi, turn it on, connect it to a USB keyboard/mouse/HDMI monitor or TV, and log in for the first time.

When you log in, go to Raspberry Pi configuration and Enable SSH. Then connect to WiFi (and open terminal to ifconfig and make a note of your IP address so you can SSH in later from another PC). Then turn on your bluetooth speaker and pair it with the Raspberry Pi. Sound will work at this point, but you can verify it by getting any audio clip online and attempting to play it.

You probably have an idea of the audio file you want to play when you open your door. It doesn't matter what the file is called, as long as it is a .wav format. Drop the audio file(s) into the /home/pi/Music/ folder. The software will play anything in that folder by the end of the project, selected at random.

Make a new folder /home/pi/PythonCode/

And inside the folder make a python file called hellorich.py

Copy the code linked on my GitHub and paste it into hellorich.py

There are a few libraries referenced in the Python code that don't come with the Pi. pip install each one from terminal.

Open terminal and type: cd /home/pi/PythonCode

Make the python file executable with: sudo chmod 755 hellorich.py

You can check if the file is executable by double clicking. You'll be prompted if you want to execute the code or open as text. If you see something like that, you're good to move forward.

Execute the code. If you did all the hardware setup already, and you plugged in the chime, you should be able to hear your audio file(s) play when you mess with the door sensor (if it's already mounted to your door, open and close the door. Otherwise you can simulate the effect by operating the sensor with your bare hands). If you hear audio, then we're almost done.

The last step is to make this Python script run every time the Raspberry Pi boots up (because you don't want to have to manually run it every time you turn the Pi on).

One of many ways to do this (but one of relatively few if you want it to work with Bluetooth audio) is to run the script as a service by placing special configuration settings into the init.d folder.

We can do this by following SCPhillips blog post for running our Python code as a service, which you don't need to click on to finish this tutorial, but if you run into any snags the post has a great troubleshooting section.

In the /home/pi/PythonCode/ folder make a file called runhellorich.sh and copy and paste the code from my GitHub into it. Save the file and close it.

Next, open terminal, cd into /home/pi/PythonCode and type: sudo cp runhellorich.sh /etc/init.d

We need to sudo because init.d will prevent you from copying the file over otherwise.

Go ahead and delete the runhellorich.sh copy in the PythonCode folder. We don't need it anymore.

cd into /etc/init.d and type: sudo chmod 755 runhellorich.sh

Then type: sudo update-rc.d myservice.sh defaults

Then type: reboot

This will reboot the machine which will automatically pair with the Bluetooth speaker and also start running the Python code in the background. And you're done! Great work, team.

If you or your Rich can't leave the chime/Raspberry Pi connected to a mouse/keyboard/monitor but want to shut this down later, you can pull the USB power supply from the Pi (not the wall due to oddities with transient currents) and risk it breaking (though you'll probably be fine doing this for a while if you don't care all that much), but you're much better off SSH'ing into the Pi from your favorite laptop and typing: sudo poweroff

I the default user is pi and the password is whatever you set it to be when you first logged into your Pi (default is raspberry).

I intentionally left some small gaps because the detailed specifics of a project like this probably won't apply to readers for very long but if there is anything you think I should add or update, please feel free to let me know here or in the issues section of the code on GitHub!
Thanks for reading!

Special shout out to Austin, who played the role of Third Buddy in the making of this instructacomic! Your support in identifying the electrical characteristics of the Pi and soundboarding ideas for how to connect it to the chime were greatly appreciated!

![Slide10](https://github.com/asa55/HelloRich/blob/master/slides/Slide10.png)
