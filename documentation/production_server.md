# Accessing and setting up the production server

## Accessing the server

Production server is running on [https://hggd.cs.helsinki.fi/](https://hggd.cs.helsinki.fi/hggd/index). To get access, ask for permissions to grp-cs-hggd-server IAM user group. A group admin can add you in the university's group management tool: [https://idm.helsinki.fi/web/](https://idm.helsinki.fi/web/). The server can be entered from the university network with ssh-connection, for example:

```bash
ssh -J melkinpaasi.cs.helsinki.fi hggd.cs.helsinki.fi
```

Program is currently running in a docker container in `/home/HGGD/`. The correct place for dataset folders is `/home/HGGD/data` and for user generated html-pages `/home/HGGD/user_templates`. There is a reverse proxy running with [Caddy](https://caddyserver.com/) in a docker container in `/home/caddy/`. To automate changes in images, [watchtower](https://containrrr.dev/watchtower/) checks for changes in dockerhub and updates the images. It is running in a docker container in `/home/watchtower`.

## Setting up the server

This is how to set up the server again in case of moving it to another server or in case of the server breaking down completely. If the server is up and running there is no need to do this.

1. Install Docker for the server ([tutorial for ubuntu](https://www.simplilearn.com/tutorials/docker-tutorial/how-to-install-docker-on-ubuntu)).
2. Pull the program image from dockerhub with `sudo docker pull hggd/test`.
3. Copy the [production docker-compose file](https://github.com/Helsinki-Genomic-Graph-Database/HGGD/blob/main/docker-compose.prod.yml) in your `HGGD` -folder and make a directories named `data` and `user_templates` there.
4. Set up the reverse proxy in `caddy` -folder by pulling the caddy docker image with `sudo docker pull caddy`.
5. Copy the [caddy docker-compose file](https://github.com/Helsinki-Genomic-Graph-Database/HGGD/blob/main/documentation/docker-compose.caddy.yml) and the [Caddyfile](https://github.com/Helsinki-Genomic-Graph-Database/HGGD/blob/main/documentation/Caddyfile) in the folder and make a directory named `sites` there. Also make a html-file named `index.html` in the directory.
6. Set up a [docker network](https://docs.docker.com/network/bridge/) with `sudo docker network create hggd_network`.
7. Connect the hggd and caddy images with `sudo docker network connect hggd_network hggd` and `sudo docker network connect hggd_network caddy`.
8. Start the containers with `sudo docker-compose up -d caddy` and `sudo docker-compose up -d hggd`. The server should now be running.
9. Set up Watchtower with `sudo docker pull containrrr/watchtower` and add the [docker-compose file](https://github.com/Helsinki-Genomic-Graph-Database/HGGD/blob/main/documentation/docker-compose.watchtower.yml) in the `watchtower` directory. Run it with `sudo docker-compose up -d watchtower`. (optional)

Adding files to the server is documented in the [user manual](https://github.com/Helsinki-Genomic-Graph-Database/HGGD/blob/main/documentation/user_manual.md).
