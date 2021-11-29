library(readxl)

dados <- read_excel("C:/Users/mairo/OneDrive/IGTI/Disciplinas_Bootcamp/EAM_Fundamentos_de_Aprendizado_de_Maquina/Dataset_Classificacao_Contratacao_TP.xlsx")

dados$Classe <- factor(dados$Classe, levels = c('Ruim','Boa'))

boxplot(dados$Prova_Logica ~ dados$Classe)


df2 <- dados %>% 
  group_by(Estado_Civil,Classe) %>% 
  tally() %>% 
  mutate(percentage = n / sum(n) * 100)

ggplot(df2, aes(Estado_Civil, percentage, fill = Estado_Civil,
)) + 
  geom_bar(stat = 'identity') +
  facet_grid(. ~ Classe) +
  ggtitle("Relacao entre Estado Civil e Classe")



df2 <- dados %>% 
  group_by(Escolaridade,Classe) %>% 
  tally() %>% 
  mutate(percentage = n / sum(n) * 100)


ggplot(dados, aes(y = Prova_Logica,x = Classe)) + geom_boxplot() 
ggplot(dados, aes(y = Redacao,x = Classe)) + geom_boxplot() 
ggplot(dados, aes(y = Psicotecnico,x = Classe)) + geom_boxplot() 
ggplot(dados, aes(y = Fit_Cultural,x = Classe)) + geom_boxplot() 
ggplot(dados, aes(y = Ingles,x = Classe)) + geom_boxplot() 
ggplot(dados, aes(y = Avaliacao_RH,x = Classe)) + geom_boxplot() 





fit <- glm(Classe ~ Prova_Logica + Redacao + Auto_Avaliacao,
           data = dados,
           family = binomial)

summary(fit)

probabilidade <- predict(fit, newdata = dados , type = 'response')

View(data.frame(select(dados,Prova_Logica,Redacao,Auto_Avaliacao,Classe),probabilidade))

Predicao <- ifelse(probabilidade >= 0.5,'Boa','Ruim')

View(data.frame(select(dados,Prova_Logica,Redacao,Auto_Avaliacao,Classe),probabilidade,Predicao))


fit <- glm(Classe ~ .,
           data = dados,
           family = binomial)

fit <- step(fit, direction = 'both')

summary(fit)
