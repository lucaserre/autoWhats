# 📲 AutoWhats – Envio Automático de Mensagens via WhatsApp

Este projeto automatiza o envio de mensagens personalizadas via WhatsApp para contatos extraídos de uma planilha Excel. É ideal para empresas que desejam enviar lembretes de cobrança, notificações ou mensagens personalizadas em massa, com praticidade e agendamento.

---

## 🚀 Funcionalidades

- Leitura de dados (nome, número, valor, data) a partir de um arquivo Excel.
- Formatação e tratamento de números telefônicos para o padrão do WhatsApp.
- Envio automático de mensagens usando o [pywhatkit](https://github.com/Ankit404butfound/pywhatkit).
- Agendamento preciso com intervalos entre mensagens.
- Logs de execução para facilitar o acompanhamento.

---

## 🛠️ Pré-requisitos

Antes de executar o projeto, certifique-se de ter instalado:

- Python 3.8+
- WhatsApp Web com sessão ativa no navegador
- As seguintes bibliotecas Python:

```bash
pip install pandas pywhatkit openpyxl
```

---

## 📁 Estrutura da Planilha

O sistema espera um arquivo Excel com pelo menos as seguintes colunas:

| CONTRATO  |   CESSIONÁRIO  |   CONTATO    |  PARCELAS  |
|-----------|----------------|--------------|------------|
|200/0588   | JOSE DAS COVES | 21999999999  |     59     |

---

## ⚙️ Como Usar

1. **Ative seu ambiente virtual (opcional):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
   ```

2. **Execute o script:**
   ```bash
   python autoWhats.py
   ```

3. **Aguarde a abertura do WhatsApp Web.**
   - Deixe a janela do navegador ativa.
   - O envio será feito automaticamente com intervalo de tempo entre cada mensagem.

---

## 💡 Exemplo de Mensagem Enviada

```
Olá João Silva! Tudo bem?
Estamos entrando em contato para informar que foi identificado um débito em aberto no valor de R$150,00 com vencimento em 10/04/2025.
Entre em contato para regularizar.
```

---

## ⚠️ Observações

- É necessário que o WhatsApp Web esteja ativo e logado.
- Certifique-se de que os números incluam o DDD e estejam no formato correto (ex: 21999999999).
- Recomendado testar com poucos contatos antes de utilizar em massa.

---

## 📄 Licença

Este projeto é de uso livre e pode ser adaptado conforme as necessidades. Recomenda-se sempre verificar os limites e políticas do WhatsApp antes de uso intensivo.
