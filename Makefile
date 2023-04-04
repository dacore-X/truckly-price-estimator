build:
	docker build -t price-estimator-service .
run:
	docker run -d --name priceService -p 8001:8001 price-estimator-service
start:
	docker start priceService
stop:
	docker stop priceService
