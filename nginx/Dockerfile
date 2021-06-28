FROM nginx:latest

#Install Prereqs
RUN apt-get update -qq && \
    apt install  -qq -y --no-install-recommends --no-install-suggests \
    ca-certificates      \
    automake             \
    autoconf             \
    build-essential      \
    libcurl4-openssl-dev \
    libpcre++-dev        \
    libtool              \
    libxml2-dev          \
    libyajl-dev          \
    lua5.2-dev           \
    git                  \
    pkgconf              \
    ssdeep               \
    libgeoip-dev         \
    libssl-dev           \
    libpcre3             \
    libpcre3-dev         \
    zlib1g               \
    zlib1g-dev           \
    wget             &&  \
    apt-get clean && rm -rf /var/lib/apt/lists/*

#Install ModSecurity
RUN git clone --depth 1 -b v3/master --single-branch https://github.com/SpiderLabs/ModSecurity
RUN cd ModSecurity && \
git submodule init && \
git submodule update && \
./build.sh && \
./configure && \
make && \
make install  && \
cd ..

#Install NGINX Connector
RUN git clone --depth 1 https://github.com/SpiderLabs/ModSecurity-nginx.git && \
#RUN cd /opt && \
git clone --recursive https://github.com/google/ngx_brotli.git
#COPY --from=modsecurity-build /usr/local/modsecurity/ /usr/local/modsecurity/
#RUN ls

RUN ver="$(nginx -v 2>&1 | awk -F/ '{print $2}')" && \
wget http://nginx.org/download/nginx-${ver}.tar.gz && \
tar zxvf nginx-${ver}.tar.gz && \
cd nginx-${ver} && \
./configure \
        --with-compat \
        #--prefix=/usr/local/nginx \
        #--sbin-path=/usr/local/nginx/nginx \
        #--modules-path=/usr/local/nginx/modules \
        #--conf-path=/etc/nginx/nginx.conf \
        #--error-log-path=/var/log/nginx/error.log \
        #--http-log-path=/var/log/nginx/access.log \
        #--pid-path=/run/nginx.pid \
        #--lock-path=/var/lock/nginx.lock \
        #--user=www-data \
        #--group=www-data \
        #--with-pcre-jit \
        #--with-file-aio \
        #--with-threads \
        #--with-http_addition_module \
        #--with-http_auth_request_module \
        #--with-http_flv_module \
        #--with-http_gunzip_module \
        #--with-http_gzip_static_module \
        #--with-http_mp4_module \
        #--with-http_random_index_module \
        #--with-http_realip_module \
        #--with-http_slice_module \
        #--with-http_ssl_module \
        #--with-http_sub_module \
        #--with-http_stub_status_module \
        #--with-http_v2_module \
        #--with-http_secure_link_module \
        #--with-stream \
        #--with-stream_realip_module \
        --add-dynamic-module=../ModSecurity-nginx \
        --add-dynamic-module=../ngx_brotli && \
        #--with-cc-opt='-g -O2 -specs=/usr/share/dpkg/no-pie-compile.specs -fstack-protector-strong -Wformat -Werror=format-security -Wp,-D_FORTIFY_SOURCE=2 -fPIC' \
        #--with-ld-opt='-specs=/usr/share/dpkg/no-pie-link.specs -Wl,-z,relro -Wl,-z,now -Wl,--as-needed -pie' \
        #--with-http_dav_module && \
#make && \
#make install && \
make modules && \
cp objs/ngx_http_modsecurity_module.so /etc/nginx/modules && \
cp objs/ngx_http_brotli_filter_module.so /etc/nginx/modules && \
cp objs/ngx_http_brotli_static_module.so /etc/nginx/modules
#OWASP CRS
RUN wget https://github.com/SpiderLabs/owasp-modsecurity-crs/archive/v3.0.2.tar.gz && \
tar -xzvf v3.0.2.tar.gz && \
mv owasp-modsecurity-crs-3.0.2 /usr/local && \
cd /usr/local/owasp-modsecurity-crs-3.0.2 && \
cp crs-setup.conf.example crs-setup.conf && \
cd rules && \
mv REQUEST-900-EXCLUSION-RULES-BEFORE-CRS.conf.example REQUEST-900-EXCLUSION-RULES-BEFORE-CRS.conf && \
mv RESPONSE-999-EXCLUSION-RULES-AFTER-CRS.conf.example RESPONSE-999-EXCLUSION-RULES-AFTER-CRS.conf

#RUN ls /usr/local/owasp-modsecurity-crs-3.0.2/rules
#ModSecurity Config
RUN mkdir /etc/nginx/modsec && \
wget -P /etc/nginx/modsec/ https://raw.githubusercontent.com/SpiderLabs/ModSecurity/v3/master/modsecurity.conf-recommended && \
mv /etc/nginx/modsec/modsecurity.conf-recommended /etc/nginx/modsec/modsecurity.conf
RUN cp ModSecurity/unicode.mapping /etc/nginx/modsec
RUN sed -i 's/SecRuleEngine DetectionOnly/SecRuleEngine On/' /etc/nginx/modsec/modsecurity.conf

