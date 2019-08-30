all: clean run
stop:
	docker container stop mmda-backend
clean:
	docker container rm mmda-backend
build:
	docker build -t mmda-backend ./mmda-backend
run:
	docker run -ti --name mmda-backend -e CQP_REGISTRY_PATH=/opt/cwb/registry -v /media/jonas/Data/wectors/:/opt/wectors/ -v /media/jonas/Data/corpora/:/opt/cwb/ -p 5000:5000 mmda-backend

