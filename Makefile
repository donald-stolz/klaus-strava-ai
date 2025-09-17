SHELL := /bin/bash
.SILENT: deploy

bundle:
	echo "Downloading dependencies..."
	pip3 install -qr requirements.txt -t dep
	echo "Bundling dependencies..."
	(cd dep && zip -rq ../function.zip .)
	rm -rf dep
	echo "Bundling API files..."
	(cd api && zip -ruq ../function.zip .)
	echo "function.zip created"

deploy:
	echo "Deploying to AWS..."
	@-terraform -chdir=terraform apply -auto-approve -var-file="prod.tfvars"
	echo "Deployment complete"