mkdir -p ~/.streamlit/


echo "\
[general]\n\
email = \"{your_email_id}\"\n\
" > ~/.streamlit/credentials.toml


echo "\
[server]\n\
headless = true\n\
enableCORS=false\n\port = $PORT\n\
" > ~/.streamlit/config.toml
