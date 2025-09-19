# TaskMaster Local

**TaskMaster Local** é uma plataforma inovadora de micro-tarefas e serviços locais que conecta pessoas que precisam de ajuda com profissionais qualificados em sua região. O aplicativo foi projetado com foco em simplicidade, eficiência e geração de receita através de um modelo de comissão por transação.

## 🚀 Aplicativo Online

**Acesse o aplicativo:** [https://w5hni7cpx7o9.manus.space](https://w5hni7cpx7o9.manus.space)

## 📱 Funcionalidades Principais

### Para Clientes
- **Publicação de Tarefas**: Crie tarefas detalhadas com preço, localização e prazo
- **Busca e Filtros**: Encontre profissionais por categoria, localização e avaliação
- **Sistema de Mensagens**: Comunique-se diretamente com os taskers
- **Avaliações**: Avalie e seja avaliado após cada serviço
- **Pagamento Seguro**: Sistema integrado de pagamentos com proteção

### Para Taskers (Prestadores de Serviço)
- **Perfil Profissional**: Crie um perfil detalhado com suas habilidades
- **Candidatura a Tarefas**: Aplique para tarefas que correspondem ao seu perfil
- **Gestão de Agenda**: Organize seus trabalhos e horários
- **Histórico de Trabalhos**: Acompanhe seu desempenho e ganhos
- **Sistema de Reputação**: Construa sua reputação através de avaliações

## 💰 Modelo de Negócio

- **Comissão por Transação**: 15% sobre cada tarefa concluída
- **Receita Recorrente**: Ganhos automáticos a cada transação
- **Escalabilidade**: Crescimento proporcional ao número de usuários
- **Múltiplas Categorias**: Diversificação de receita através de diferentes serviços

## 🛠 Tecnologias Utilizadas

### Frontend
- **React 18** - Interface de usuário moderna e responsiva
- **Tailwind CSS** - Estilização eficiente e customizável
- **React Router** - Navegação entre páginas
- **Heroicons** - Ícones consistentes e profissionais

### Backend
- **Flask** - Framework web Python robusto e flexível
- **SQLAlchemy** - ORM para gerenciamento de banco de dados
- **Flask-JWT-Extended** - Autenticação segura com tokens JWT
- **Flask-CORS** - Suporte a requisições cross-origin
- **SQLite** - Banco de dados leve e eficiente

## 🗂 Estrutura do Projeto

```
taskmaster-backend/
├── src/
│   ├── models/          # Modelos de dados
│   │   ├── user.py      # Modelo de usuário
│   │   ├── task.py      # Modelo de tarefas
│   │   ├── review.py    # Sistema de avaliações
│   │   ├── message.py   # Sistema de mensagens
│   │   └── payment.py   # Sistema de pagamentos
│   ├── routes/          # Rotas da API
│   │   ├── auth.py      # Autenticação
│   │   ├── tasks.py     # Gerenciamento de tarefas
│   │   └── users.py     # Gerenciamento de usuários
│   ├── static/          # Frontend buildado
│   └── main.py          # Aplicação principal
├── venv/                # Ambiente virtual Python
└── requirements.txt     # Dependências
```

## 🚀 Como Executar Localmente

### Pré-requisitos
- Python 3.11+
- Node.js 18+
- Git

### Backend
```bash
cd taskmaster-backend
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou venv\Scripts\activate  # Windows
pip install -r requirements.txt
python src/main.py
```

### Frontend (Desenvolvimento)
```bash
cd taskmaster-local
npm install
npm run dev
```

## 👥 Contas de Demonstração

### Cliente
- **Email**: cliente@demo.com
- **Senha**: 123456

### Tasker
- **Email**: tasker@demo.com
- **Senha**: 123456

## 📊 Categorias de Serviços

- **Limpeza**: Limpeza residencial, pós-mudança, escritórios
- **Montagem**: Móveis, equipamentos, instalações
- **Entrega**: Documentos, compras, encomendas
- **Pet Care**: Passeios, cuidados, veterinário
- **Jardinagem**: Manutenção, paisagismo, podas
- **Tecnologia**: Suporte técnico, instalações, reparos
- **Outros**: Serviços diversos

## 🔒 Segurança

- Autenticação JWT com tokens seguros
- Validação de dados em todas as rotas
- Proteção contra ataques CORS
- Senhas criptografadas com hash seguro
- Validação de permissões por usuário

## 📈 Potencial de Mercado

O TaskMaster Local atende a um mercado em crescimento de economia compartilhada e serviços sob demanda, com potencial para:

- **Expansão Geográfica**: Replicação em diferentes cidades
- **Novas Categorias**: Adição de mais tipos de serviços
- **Parcerias**: Integração com empresas locais
- **Monetização Adicional**: Anúncios, planos premium, seguros

## 🤝 Contribuição

Este projeto foi desenvolvido como uma solução completa e funcional. Para contribuições ou melhorias, entre em contato através do repositório.

## 📄 Licença

Este projeto é propriedade intelectual e foi desenvolvido como demonstração de capacidades técnicas.

---

**Desenvolvido com ❤️ para revolucionar o mercado de serviços locais**

