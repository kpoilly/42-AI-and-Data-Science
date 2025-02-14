# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    Makefile                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: kpoilly <kpoilly@student.42.fr>            +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/05/15 13:32:57 by kpoilly           #+#    #+#              #
#    Updated: 2024/05/15 13:52:26 by kpoilly          ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

all:
	docker compose -f ./deployment/docker_compose/docker-compose.dev.yml -p onyx-stack up -d --pull always --force-recreate

clone:
	git clone git@github.com:onyx-dot-app/onyx.git

down:
	docker compose -f ./deployment/docker_compose/docker-compose.dev.yml down

clean:
	docker system prune -af

.PHONY:
	all down clear
