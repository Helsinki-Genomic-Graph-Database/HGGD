# Accessing and setting up the production server

## Accessing the server

Production server is running on [https://hggd.cs.helsinki.fi/](https://hggd.cs.helsinki.fi/hggd/index). To get access, ask for permissions to grp-cs-hggd-server -user group. Server can be entered from the university network with ssh-connection, for example:

```bash
ssh -J melkinpaasi.cs.helsinki.fi hggd.cs.helsinki.fi
```

Program is currentlys running in a docker container in `/home/HGGD/`. Datafolder for the dataset files is in `/home/HGGD/data`. There is a reverse proxy running with [Caddy](https://caddyserver.com/) in a docker container in `/home/caddy/`. To automate changes in images, [watchtower](https://containrrr.dev/watchtower/) checks for changes in dockerhub and updates the images. It is running in a docker container in `/home/watchtower`.

## Setting up the server

First install Docker for the server ([tutorial for ubuntu](https://www.simplilearn.com/tutorials/docker-tutorial/how-to-install-docker-on-ubuntu)). Pull the program image from dockerhub with `sudo docker pull hggd/test`. Copy the [production docker-compose file](https://github.com/Helsinki-Genomic-Graph-Database/HGGD/blob/main/docker-compose.prod.yml) in your `HGGD` -folder and make a directory named `data` there.

Set up the reverse proxy in `caddy` -folder by pulling the caddy docker image with `sudo docker pull caddy`. Copy the [caddy docker-compose file](https://github.com/Helsinki-Genomic-Graph-Database/HGGD/blob/main/documentation/docker-compose.caddy.yml) and the [Caddyfile](https://github.com/Helsinki-Genomic-Graph-Database/HGGD/blob/main/documentation/Caddyfile) in the folder and make a directory named `sites` there. Also make a html-file named `index.html` in the directory.

Then set up a [docker network](https://docs.docker.com/network/bridge/) with `sudo docker network create hggd_network`. Then connect the hggd and caddy images with `sudo docker network connect hggd_network hggd` and `sudo docker network connect hggd_network caddy`.

Now start the containers with `sudo docker-compose up -d caddy` and `sudo docker-compose up -d hggd` and the server should now be running.

Watchtower can be set up with `sudo docker pull containrrr/watchtower` and adding the [docker-compose file](https://github.com/Helsinki-Genomic-Graph-Database/HGGD/blob/main/documentation/docker-compose.watchtower.yml) in the `watchtower` directory. It can be run with `sudo docker-compose up -d watchtower`.

Adding files to the server is documented in the [user manual](https://github.com/Helsinki-Genomic-Graph-Database/HGGD/blob/main/documentation/user_manual.md).
