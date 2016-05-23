server {
    server_name www.investperdiem.com;
    return 301 http://investperdiem.com$request_uri;
}

server {
    server_name investperdiem.com;

    access_log off;
    client_max_body_size 5M;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header X-Forwarded-Host $server_name;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header Host $http_host;
        add_header P3P 'CP="ALL DSP COR PSAa PSDa OUR NOR ONL UNI COM NAV"';
    }
}
