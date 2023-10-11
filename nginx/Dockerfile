FROM nginx:alpine
ADD nginx/default.conf /etc/nginx/conf.d
RUN ln -snf /usr/share/zoneinfo/Asia/Kuala_Lumpur /etc/localtime && echo Asia/Kuala_Lumpur > /etc/timezone