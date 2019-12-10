# Front platform 

- For this proyect we use tools like Dash and our own API for accesing modules that deliever data from our data base in postgres 

## Docker instructions 

- Build
    - `sudo docker build -t front_app .`
    - `sudo docker run -p 8021:8021 -d --restart=always  --name front_app front_app` 