# front_end/Dockerfile

# pull official base image
FROM node:18-slim

# set working directory
WORKDIR /app

# add `/usr/src/app/node_modules/.bin` to $PATH
ENV PATH app/node_modules/.bin:$PATH

COPY . /app/front_end
# start app
CMD ["nodejs", "index.html"]
