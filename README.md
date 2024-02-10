# Setting up the coursework (a guide)

This guide aims to help you set up the coursework either using VSCode, 
or by working on a local copy. See 
[here](#setting-up-the-coursework-with-vscode) for the former and 
[here](#setting-up-the-coursework-locally) for the latter.

After you've done that, you can go [here](#setting-up-infos) to get 
started with the coursework.

## Important note

**This is not guaranteed to work**. This is supposed to be a helpful 
guide, but I am not responsible for any long-term pain that might result
from use of this guide. **If you set up locally, I have no idea if it 
will actually let you submit**. I am 99% sure it's fine, and worst case,
just copy your files over.

------------------------------------------------------------------------

# Setting up the coursework with VSCode

## Install 'Remote - SSH'

You will need to make sure you have a working `ssh` command set up.
Refer to the lab sheet for this. It's called something like 
'infos-coursework-preliminary.pdf'. Mostly you need to worry about the 
actual NMES page for connecting to bastion.

1. Hit `Ctrl + Shift + X` to open up the extension manager
2. Search for "remote ssh" and select the first one (It should be called 
   "Remote - SSH")
3. Install it

![The actual page for installing the extension](image.png)

1. `Ctrl + Shift + P` This opens the command palette.
2. Type "Developer: Reload Window"
3. Select `Developer: Reload Window` and hit `Enter` or just clicking it
   is probably fine. **From now on, these last three steps will be 
   just written as "execute `Command` using the command palette".**

## Connecting to the OSC machine

Time to connect your VSCode workspace to the remote OSC machine. First
we set up our ssh config so that we can access the host quickly, then
we connect to it.

1. Execute `Remote-SSH: Open SSH Configuration File...` using the 
   command palette.
2. Choose the top configuration file, what exactly this file is depends
   on your OS, but hopefully the following works on any OS.
3. Copy and paste this into your config file **and save it**. Make sure
   your replace `kxxxxxxxx` with your actual k-number.

```py
# The remote host for our coursework
Host OSC
    HostName 5CCS2OSC.nms.kcl.ac.uk
    ProxyJump kxxxxxxxx@bastion.nms.kcl.ac.uk
    User kxxxxxxxx

# Set a 60 second keep alive in case there is no activity.
Host *
    ServerAliveInterval 60
```

4. Execute `Remote-SSH: Connect to Host...` using the command palette.
5. Select `OSC`
6. This should open a new window and you will be prompted to enter your
   password. 
7. See the section [Troubleshooting](#troubleshooting) for more

![Password prompt](image2.png)

## Troubleshooting

### I can't enter my password fast enough and it times out!

1. Execute `Remote-SSH: Settings` using the command palette
2. Find 'Connnect Timeout'
3. Set this to a longer duration than 15 seconds.
   1. You can also do this by adding `"remote.SSH.connectTimeout": 100`
      to your `settings.json` if you prefer. Of course, `100` is just
      an example value.

------------------------------------------------------------------------

# Setting up the coursework locally

I much prefer working on things locally. Here's how you can do that.
There are easier ways of doing this, but this should hopefully be quite
future proof against anything that might be user-specific, so I would 
recommend everyone do this, instead of just copying someone else's 
local InfOS skeleton.

1. Install a bunch of stuff...
   1. Install qemu. This is OS-specific, so work it out.
   2. Install **GCC**. Don't use Clang. InfOS invokes some undefined 
      behavior and I bet Clang actually notices.
   4. Install make.
   5. Install bash.
   6. Install git.
2. [Setup InfOS](#setting-up-infos) on the remote machine. You should 
   now have `infos`, `infos-user` and `run-infos` all in the same 
   folder. Please make sure you are in this folder.
3. From here you have two options:
   1. [Copy everything back and forth](#copy-everything-back-and-forth)
      This is basically the same as git, but without the `.gitignore`.
   2. [Use git](#use-git) This would probably be the most sensible way
      of doing things.

## Copy everything back and forth

1. Run the following commands. You don't need to do this if you already
   have a directory that contains *only these three files*. In that 
   case, just replace `coursework` with the name of that directory.

```sh
mkdir coursework
cp -r infos coursework/infos
cp -r infos-user coursework/infos-user
cp run-infos coursework/run-infos
```

2. This should have made a folder with only these three files in it.
   Then, run these commands: 

```sh
cd coursework
pwd
```

This will output a path. From now on I wall call this file path
`<coursework-path>`. Wherever you see this token, please replace it with 
the output of the above command

3. Disconnect from the remote host E.g. on Linux, press `Ctrl + D`.
4. Copy the archive to any local directory of your choice, here is a 
   template. You are copying to `<local-folder>`, which should be 
   replaced by some path on your local machine. Both `scp` and `rsync`
   versions are provided. I recommend `rsync`, it is much faster.

```sh
rsync -avz --delete -e "ssh -J kxxxxxxxx@bastion.nms.kcl.ac.uk" \
kxxxxxxxx@5CCS2OSC.nms.kcl.ac.uk:<coursework-path> \
<local-folder>
```

An example of a full command:

```sh
rsync -avz -e "ssh -J k21052695@bastion.nms.kcl.ac.uk" \
k21052695@5CCS2OSC.nms.kcl.ac.uk:/home/k21052695/coursework/ \
/home/oli/Documents/School/Coursework/OSC/coursework
```

5. We need to make everything again

```sh
cd ./coursework/infos
make
cd ../infos-user
make
make fs
``` 

6. We can't use the normal `./run-infos` Makefile, so we need to do it
   ourself. You might want to make this a script. This has been taken
   from [the InfOS repository](https://github.com/tspink/infos). I'm not
   a qemu wizard.

```sh
qemu-system-x86_64 -m 8G \
  -kernel ../infos/out/infos-kernel \
  -debugcon stdio \
  -hda bin/rootfs.tar \
  -append 'pgalloc.debug=0 pgalloc.algorithm=simple objalloc.debug=0 sched.debug=0 sched.algorithm=cfs syslog=serial boot-device=ata0 init=/usr/init'
```

![QEMU running InfOS](image-1.png)

7. Yay, you did it! But we need to be able to update the remote machine
   with our progress so that we can submit.

```sh
rsync -avz -e "ssh -J k21052695@bastion.nms.kcl.ac.uk" \
/home/oli/Documents/School/Coursework/OSC/ \
k21052695@5CCS2OSC.nms.kcl.ac.uk:/home/k21052695/coursework/
```

When you're using the remote host, you should use `./run-infos` and when
you're working locally, use `qemu-system-x86_64`. 

### Using `scp` instead of `rsync`

There are very few reasons to use `scp` instead of `rsync`, but here are
the equivalent commands, incase you really want to.

```sh
scp -r -J kxxxxxxxx@bastion.nms.kcl.ac.uk \
kxxxxxxxx@5CCS2OSC.nms.kcl.ac.uk:<coursework-path> \
<local-folder>
```

```sh
scp -r -J kxxxxxxxx@bastion.nms.kcl.ac.uk <local-folder> \
kxxxxxxxx@5CCS2OSC.nms.kcl.ac.uk:<coursework-path>
```

## Use Git

[TODO]

------------------------------------------------------------------------

# Setting up InfOS

This section is about how to set up InfOS on the remote OSC machine.

1. Connect to the remote host. Again, replace `kxxxxxxxx` with your 
   k-number.

```sh
ssh -J kxxxxxxxx@bastion.nms.kcl.ac.uk kxxxxxxxx@5CCS2OSC.nms.kcl.ac.uk
```

ssh -J kxxxxxxxx@bastion.nms.kcl.ac.uk kxxxxxxxx@5CCS2OSC.nms.kcl.ac.uk

2. Execute the following commands wherever you want to work on InfOS.
   (probably not your home directory).

```sh
git clone /shared/5CCS2OSC/infos
git clone /shared/5CCS2OSC/infos-user
cd infos && make && cd ..
ln -s /shared/5CCS2OSC/run-infos .
```

3. Execute `./run-infos`.

```sh
./run-infos
```