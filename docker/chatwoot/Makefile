include .env
export $(shell sed 's/=.*//' .env)

compose:
	@docker compose run --rm rails bundle exec rails db:setup
	@docker compose run --rm rails bundle exec rails db:chatwoot_prepare
	@docker compose up -d
