# Defund The Police

There are about 18,000 state and local police agencies in the US. Police funding is the second largest category of local government spending after education. On average, the United States spends $340 per person per year for public policing, for a total of $193 billion in spending in 2017. [Click here to learn more](https://www.urban.org/policy-centers/cross-center-initiatives/state-and-local-finance-initiative/state-and-local-backgrounders/police-and-corrections-expenditures)

When it comes to finding how much each of these departments spend individually, it can be harrowing proccessing digging through obscure documents. 

The goal of this project is to provide transparency on police budgets on a local level, and provide a social media toolkit to spread messages on how to better utilize police funding for empowering communities. 

You can view the site here
https://share.streamlit.io/banjtheman/defundthepolice/main/main_st.py

Here is some example output

![Arl budget](images/arl_budget.jpeg)
![Arl defund](images/arl_defund.jpeg)
![Arl cpu](images/arl_cpu.jpeg)

## Run Local
To start simply install requirements, and use streamlit to launch the app

```
pip install -r requirements.txt
streamlit run main_st.py
```


## 🤝 Contributing <a href = "https://discord.gg/p9dD8p5"><img alt="Discord" src="https://img.shields.io/discord/759597146076348456"></a>

Have ideas on what features to add? [Open a new issue](https://github.com/banjtheman/defundthepolice/issues/new/choose)! We need all the help we can get! You can also join the discord server to give suggestions.


## Hacktoberfest 

![Hacktoberfest](images/hf2020.png)

In order to have effective messages, we need data. This Hacktoberfest we want to collect as much data as we can from police budgets in order to create more effective messages.

There will be PRs you can do, right now that wil get us data and help spread our message.

To learn more check out their [FAQ](https://hacktoberfest.digitalocean.com/faq/)

## Dockerized applciation

To start the application first install [Docker](https://docs.docker.com/engine/install/) 
and (docker-compose)[https://docs.docker.com/compose/].

P.S: Make sure to follow post installation [steps](https://docs.docker.com/engine/install/linux-postinstall/) 
for linux distributions.

After this you can run the application using:
* `docker-compose up --build -d`

In order to look at the logs you can run:
* `docker-compose logs -f`

In order to stop the application from running on docker you can do
* `docker-compose down`
