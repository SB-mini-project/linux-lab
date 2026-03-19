"""
환경 초기화 모듈
practice/ 디렉터리를 초기 상태로 복원한다.
"""
import os
import shutil

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PRACTICE = os.path.join(_ROOT, "practice")

# ── 파일 원본 내용 ──────────────────────────────────────

ACCESS_LOG = """\
192.168.0.1 2026-03-01 08:01:00 200 1234 GET /index.html
192.168.0.2 2026-03-01 08:15:00 500 512 POST /login
192.168.0.3 2026-03-02 09:00:00 403 256 GET /dashboard
192.168.0.2 2026-03-02 10:30:00 200 1024 POST /login
192.168.0.4 2026-03-03 11:00:00 500 128 GET /api/data
192.168.0.5 2026-03-03 11:30:00 200 64 GET /health
192.168.0.6 2026-03-04 12:00:00 200 2048 GET /reports
192.168.0.7 2026-03-04 12:30:00 403 256 GET /admin
192.168.0.8 2026-03-05 13:00:00 200 512 POST /login
192.168.0.9 2026-03-05 13:15:00 502 0 GET /api/data
192.168.0.10 2026-03-06 14:00:00 200 4096 GET /dashboard
192.168.0.2 2026-03-06 14:30:00 200 128 POST /logout
192.168.0.11 2026-03-07 15:00:00 404 256 GET /index.html
192.168.0.12 2026-03-07 15:30:00 200 1024 GET /settings
192.168.0.13 2026-03-08 16:00:00 401 256 GET /admin
192.168.0.14 2026-03-08 16:30:00 200 2048 POST /api/data
192.168.0.15 2026-03-09 17:00:00 500 0 POST /login
192.168.0.16 2026-03-09 17:30:00 200 1024 GET /reports
192.168.0.17 2026-03-10 18:00:00 200 2048 GET /dashboard
192.168.0.18 2026-03-10 18:30:00 503 0 GET /backup
"""

ERROR_LOG = """\
2026-03-01 ERROR DB connection failed
2026-03-01 WARN Disk usage high
2026-03-02 ERROR Null pointer exception
2026-03-03 INFO System rebooted
2026-03-04 INFO Daily backup completed
2026-03-04 WARN CPU usage high
2026-03-05 ERROR API timeout on /reports
2026-03-05 WARN Memory usage above threshold
2026-03-06 INFO User sync completed
2026-03-06 ERROR Failed to write audit log
2026-03-07 INFO Log rotation completed
2026-03-07 WARN SSL certificate expires soon
2026-03-08 ERROR Payment service unavailable
2026-03-09 WARN Too many login attempts
2026-03-09 ERROR Cache server not reachable
2026-03-10 INFO Maintenance mode disabled
"""

SECURE_LOG = """\
2026-03-01 08:01:00 server sshd 1001 pam session auth SUCCESS for user1 from 192.168.0.1
2026-03-01 08:05:00 server sshd 1002 pam session auth FAILED for user2 from 192.168.0.2
2026-03-01 08:10:00 server sshd 1003 pam session auth FAILED for user3 from 192.168.0.3
2026-03-02 09:00:00 server sshd 1004 pam session auth SUCCESS for user1 from 192.168.0.1
2026-03-02 09:30:00 server sshd 1005 pam session auth SUCCESS for user4 from 192.168.0.4
2026-03-03 10:00:00 server sshd 1006 pam session auth SUCCESS for user2 from 192.168.0.2
2026-03-03 10:15:00 server sshd 1007 pam session auth FAILED for user5 from 192.168.0.5
2026-03-04 11:00:00 server sshd 1008 pam session auth SUCCESS for admin1 from 192.168.0.10
2026-03-04 11:30:00 server sshd 1009 pam session auth FAILED for user6 from 192.168.0.6
2026-03-05 12:00:00 server sshd 1010 pam session auth SUCCESS for user7 from 192.168.0.7
2026-03-05 12:30:00 server sshd 1011 pam session auth SUCCESS for user3 from 192.168.0.3
2026-03-06 13:00:00 server sshd 1012 pam session auth FAILED for admin2 from 192.168.0.11
2026-03-06 13:30:00 server sshd 1013 pam session auth SUCCESS for user8 from 192.168.0.8
2026-03-07 14:00:00 server sshd 1014 pam session auth FAILED for user9 from 192.168.0.9
2026-03-07 14:30:00 server sshd 1015 pam session auth SUCCESS for user10 from 192.168.0.12
"""

USER_LIST = """\
1001,Kim,Sales,Manager
1002,Lee,IT,Staff
1003,Park,HR,Staff
1004,Choi,IT,Manager
1005,Jung,Finance,Staff
1006,Kang,Marketing,Staff
1007,Han,Sales,Staff
1008,Yoon,Security,Manager
1009,Lim,IT,Staff
1010,Shin,HR,Manager
1011,Seo,Finance,Manager
1012,Hong,Marketing,Staff
"""

SERVER_INFO = """\
web01\t10.0.0.1\tSeoul-DC-A
web02\t10.0.0.4\tSeoul-DC-B
db01\t10.0.0.2\tBusan-DC-A
db02\t10.0.0.5\tBusan-DC-B
app01\t10.0.0.3\tSeoul-DC-A
app02\t10.0.0.6\tSeoul-DC-B
cache01\t10.0.0.7\tIncheon-DC-A
batch01\t10.0.0.8\tDaejeon-DC-A
backup01\t10.0.0.9\tDaegu-DC-A
proxy01\t10.0.0.10\tSeoul-DC-A
"""

DOCKER_COMPOSE = """\
services:
  #nextcloud
  nc_server:
    image: linuxserver/nextcloud:amd64-latest
    container_name: nc_server
    restart: unless-stopped
    ports:
      - 4432:443
    volumes:
      - /zfs/nextcloud/config:/config
      - /zfs/nextcloud/data:/data
      - /zfs/storage/Drive:/drive
    environment:
      - PUID=${OPR_UID}
    - PGID=${OPR_GID}
      - TZ=UTC
      - DOCKER_MODS=linuxserver/mods:nextcloud-notify-push
    labels:
      - "d2n.enabled=true"
      - "d2n.database=Docker"
    depends_on:
      - nc_mariadb
      - nc_redis
  #mariadb
  nc_mariadb:
    image: linuxserver/mariadb:amd64-latest
    container_name: nc_mariadb
    restart: unless-stopped
    volumes:
      - /docker/nextcloud_mariadb/config:/config
    environment:
      - PUID=${OPR_UID}
      - PGID=${OPR_GID}
      - TZ=UTC
      - MYSQL_ROOT_PASSWORD=${MYSQL_ROOT_PASSWORD}
      - MYSQL_DATABASE=${DB_NAME}
      - MYSQL_USER=${DB_USER}
      - MYSQL_PASSWORD=${DB_PASSWORD}
    labels:
      - "d2n.enabled=true"
      - "d2n.database=Docker"
    healthcheck:
      test: ["CMD", "mariadb-admin", "ping", "-h", "localhost", "-u", "root", "--password=$${DB_PASSWORD}"]
      interval: 30s
      timeout: 5s
      retries: 5
  #redis
  nc_redis:
    image: docker.io/redis:latest
    container_name: nc_redis
    restart: unless-stopped
    user: ${OPR_UID}:${OPR_GID}
    volumes:
      - /docker/nextcloud_redis/data:/data
    environment:
      - UID=${OPR_UID}
      - GID=${OPR_GID}
      - TZ=UTC
      - REDIS_PASSWORD=${DB_PASSWORD}
    labels:
      - "d2n.enabled=true"
      - "d2n.database=Docker"
    command: ['/bin/sh', '-c', 'redis-server --appendonly yes --requirepass $${REDIS_PASSWORD}']
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 30s
      timeout: 5s
      retries: 5
  #imaginary
  nc_imaginary:
    image: nextcloud/aio-imaginary:latest
    container_name: nc_imaginary
    command: >
      -enable-url-source
      -p 9000
      -concurrency 18
      -http-read-timeout 60
      -http-write-timeout 60
      -max-allowed-resolution 50
      -cpus 6
    restart: unless-stopped
    labels:
      - "d2n.enabled=true"
      - "d2n.database=Docker"
"""

# ── 초기화 함수 ────────────────────────────────────────

def reset_practice():
    """practice/ 디렉터리를 초기 상태로 복원"""
    # 기존 삭제 후 재생성
    if os.path.exists(PRACTICE):
        shutil.rmtree(PRACTICE)

    os.makedirs(os.path.join(PRACTICE, "logs"))
    os.makedirs(os.path.join(PRACTICE, "data"))

    _w("logs/access.log",          ACCESS_LOG)
    _w("logs/error_202603.log",    ERROR_LOG)
    _w("logs/secure.log",          SECURE_LOG)
    _w("data/user_list.csv",       USER_LIST)
    _w("data/server_info.tsv",     SERVER_INFO.replace("\\t", "\t"))
    _w("data/docker-compose.yml",  DOCKER_COMPOSE)

def _w(rel, content):
    path = os.path.join(PRACTICE, rel)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
