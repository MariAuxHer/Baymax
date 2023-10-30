# nginx/Dockerfile

FROM nginx:latest
WORKDIR /app
COPY nginx/nginx.conf /etc/nginx/nginx.conf

# statically host the entire front end
COPY front_end /app/front_end

# remember to run collectstatic in the back_end so all the static assets are present
# generate static files from the back end and copy into nginx server
COPY back_end/static /app/static
