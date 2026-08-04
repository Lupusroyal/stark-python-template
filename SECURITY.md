# Security Policy

## Supported Versions

As correções de segurança são aplicadas apenas à versão estável mais recente do projeto.

| Version | Supported |
|----------|-----------|
| Latest   | ✅ |
| Older    | ❌ |

---

# Reporting a Vulnerability

Se você encontrar uma vulnerabilidade de segurança, por favor **não abra uma Issue pública**.

Em vez disso:

- descreva o problema;
- informe como reproduzir;
- explique o possível impacto;
- forneça evidências, se possível.

O mantenedor analisará o relatório e responderá o mais rápido possível.

---

# Security Best Practices

Ao utilizar este template em produção, recomenda-se:

- utilizar uma `SECRET_KEY` forte e exclusiva;
- manter as dependências atualizadas;
- utilizar HTTPS;
- configurar corretamente CORS e Trusted Hosts;
- revisar periodicamente permissões e papéis (RBAC);
- proteger credenciais utilizando variáveis de ambiente;
- nunca publicar arquivos `.env` ou chaves privadas.

---

# Responsible Disclosure

Vulnerabilidades reportadas de forma responsável serão investigadas antes de qualquer divulgação pública.

Caso confirmadas, serão corrigidas em uma nova versão do projeto.
