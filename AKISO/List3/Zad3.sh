#!/bin/bash

CAT_API_URL="https://api.thecatapi.com/v1/images/search"
CHUCK_NORRIS_API_URL="https://api.chucknorris.io/jokes/random"

echo "Downloading image"
cat_response=$(curl -s "$CAT_API_URL")
cat_url=$(echo "$cat_response" | jq -r '.[0].url')

echo "Downloading quote..."
chuck_response=$(curl -s "$CHUCK_NORRIS_API_URL")
chuck_joke=$(echo "$chuck_response" | jq -r '.value')

echo "Image:"
curl -s ${cat_url} | catimg -w 200 -

echo ""
echo "Quote:"
echo "$chuck_joke"
