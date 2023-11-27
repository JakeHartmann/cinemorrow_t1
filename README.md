
# Trabalho T2: Modelagem e Implementação
**PROBLEMA**:
Implementar um sistema orientado a objetos em Python com o intuito de organizar grupos para assistir determinados tipos de mídias.
Dessa vez, com interface gráfica.
 


## ESCOPO DO DESENVOLVIMENTO:
O propósito de Cinemorrow é facilitar a organização de diferentes pessoas com o objetivo de assistir a filmes e séries, portanto isso impõe a ideia de cadastros, assim como a listagem, remoção, e alteração de pessoas, mídias e grupos.
Uma tela inicial apresentará ao utilizador do sistema diferentes opções:
- Gerenciar Mídias
- Gerenciar Pessoas
- Gerenciar Grupos
- Relatórios

## Gerenciar Midias

Uma mídia consiste em uma classe abstrata a qual subclasses como filmes e séries herdam seus atributos básicos. Portanto, na tela da gerência de mídias, o usuário terá as seguintes opções:

- Adicionar Mídia: onde o usuário deverá especificar o tipo de mídia a ser adicionado, seu título e opcionalmente, caso seja uma série, o número de temporadas tal como o número de episódios
- Remover Mídia: a listagem de mídias ocorreria, e um índice associado à mídia serviria de identificador para a sua exclusão
- Alterar Mídia: novamente, a listagem de mídias ocorreria, e o usuário terá a opção de escolher o índice associado à mídia e modificar seus atributos
- Listar Mídias: a listagem das mídias cadastradas ocorre

## Gerenciar Pessoas

Uma pessoa possui um nome, um e-mail e opcionalmente, um tipo de mídia favorito.
- Adicionar Pessoa: é solicitado ao usuário o nome da pessoa, seu e-mail e opcionalmente, seu tipo de mídia favorito.
- Remover Pessoa: a listagem de pessoas ocorreria, e um índice associado à pessoa serviria de identificador para a sua opcional exclusão
- Alterar Pessoa: novamente, a listagem de pessoas ocorreria, e o usuário terá a opção de escolher o índice associado à pessoa e modificar suas informações
- Listar Pessoas: a listagem das pessoas cadastradas ocorre

## Gerenciar Grupos

Um grupo é uma agregação de pessoas, possui um nome e uma única mídia associada.
- Adicionar Grupo: é solicitado ao usuário o nome do grupo, um integrante base, uma mídia associada e uma data para a sessão
- Remover Grupo: a listagem de grupos ocorre, e um índice associado ao grupo serviria de identificador para a sua opcional exclusão
- Alterar Grupo: novamente, a listagem de grupos ocorreria, e o usuário terá a opção de escolher o índice associado ao grupo, podendo então realizar algumas ações
    - Alterar Nome (altera o nome do grupo)
    - Adicionar Membro (uma pessoa pode ser adicionada ao grupo)
    - Remover Membro (a listagem de pessoas incluídas no grupo ocorre e um índice associado à determinada pessoa serve de identificador para sua opcional exclusão)
    - Alterar Data da Próxima Sessão ()
- Listar Grupos: a listagem de grupos cadastrados ocorre, e próximo de cada grupo será mostrado a sua data associada, além do seu progresso caso possível. Isto é, caso o tipo de mídia associada ao grupo seja uma série, a porcentagem de episódios já assistidos será mostrada, tal como o número de episódios restantes

## Relatórios

Os relatórios consistem em estatísticas básicas envolvendo o número de ocorrências de certo atributo, como por exemplo o tipo de mídia mais favorito.
## Regras de Negócio

Um grupo só poderá ter uma mídia regente.

## Escopo

O sistema oferece uma interface gráfica e persistência de dados.

## Considerações

- Cadastros: tipos diferentes de mídia, pessoas e grupos
- Registros: número de vezes que um relatório foi gerado
- Relatórios: 
    - Tipo de mídia favorita mais comum;

## Bugs Conhecidos:

- Exemplo fictício: caso exista um grupo com a mídia associada "Oppenheimer" e o usuário alterar o nome da mídia para "Barbie", tudo ocorre normalmente. Agora, caso o usuário mude mais uma vez para "Interstellar", por exemplo, a listagem de grupos irá listar a mídia associada ainda como "Barbie".