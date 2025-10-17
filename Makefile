SHELL := /bin/bash
.SILENT: bundle deploy

bundle:
	echo "Downloading dependencies..."
	pip3 install -qr requirements.txt -t dep
	echo "Bundling dependencies..."
	(cd dep && zip -rq ../function.zip .)
	rm -rf dep
	echo "Bundling API files..."
	(cd api && zip -ruq ../function.zip . || [ $$? -eq 12 ])
	echo "function.zip created"

deploy: bundle
	echo "Deploying to AWS..."
	terraform -chdir=terraform apply -auto-approve -var-file="prod.tfvars"
	echo "Deployment complete"

dev:
	fastapi dev api/main.py