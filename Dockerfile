FROM kalilinux/kali-linux-docker:latest

RUN echo 'deb http://old.kali.org/kali sana main non-free contrib' >> /etc/apt/sources.list \
 && echo 'deb-src http://old.kali.org/kali sana main non-free contrib' >> /etc/apt/sources.list \
 && echo 'deb http://http.kali.org/kali kali-rolling main contrib non-free' >> /etc/apt/sources.list \
 && echo 'deb-src http://http.kali.org/kali kali-rolling main contrib non-free' >> /etc/apt/sources.list \
 && apt-get update

RUN echo 'APT::Get::Install-Recommends "false";' >> /etc/apt/apt.conf \
 && echo 'APT::Get::Install-Suggests "false";' >> /etc/apt/apt.conf

 RUN apt-get install -y \
 		metasploit-framework \
 		zenity \
 		gcc \
 		mingw32 \
 		backdoor-factory \
 		monodevelop \
 		ruby \
 		apache2 \
   upx-ucl \
   xterm \
   gnome-terminal \
   default-jre \
   default-jdk \
   unzip \
   aapt \ 
   apktool \
   dex2jar \
   zlib1g-dev \
   libmagickwand-dev \
   imagemagick \
   zipalign

WORKDIR /root/TheFatRat
ADD . ./

RUN chmod +x ./fatrat

CMD ["./fatrat"]
