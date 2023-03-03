for i in {8001..8010}
do
	docker run -d -e RABBIT_HOST=172.20.10.2 -e QUEUE_NAME=games -e PORT=$i --name request_$i request
done
docker ps -a
