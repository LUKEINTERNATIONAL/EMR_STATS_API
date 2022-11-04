.PHONY: build build-m1 push

DOCKER_TAG := emr_stats_api_backend:x86
SERVER_ADDR := 192.168.11.106
USERNAME := emr_monitor

build:
	docker build -t $(DOCKER_TAG) .

build-m1:
	docker buildx build -t "$(DOCKER_TAG)" --platform linux/amd64 .

push:
	docker save -o /tmp/backend.tar $(DOCKER_TAG)
	scp /tmp/backend.tar $(USERNAME)@$(SERVER_ADDR):~/
	ssh $(USERNAME)@$(SERVER_ADDR) docker load -i /home/$(USERNAME)/backend.tar
	rm /tmp/backend.tar
