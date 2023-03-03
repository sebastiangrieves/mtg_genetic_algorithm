for i in {8001..8010}
do
	docker stop request_$i
	docker rm request_$i
done
docker ps -a