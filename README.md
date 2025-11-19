# Sistema Inteligente de Controle e Monitoramento de Lâmpadas via IoT

Este repositório contém o código-fonte, a documentação, esquemas e resultados do projeto de automação de iluminação para ambientes domésticos, focado em proporcionar conforto e redução de ansiedade via controle inteligente de cor e brilho.

## Funcionalidades
- Controle dinâmico da iluminação (brilho/temperatura) por potenciômetro analógico
- Comunicação assíncrona entre os módulos via MQTT (broker público)
- Simulação completa nas plataformas (https://wokwi.com/projects/447923693002369025 , https://wokwi.com/projects/447924455020686337 e https://www.hivemq.com/demos/websocket-client/)
- Código-fonte organizado por publisher e subscriber
- Gravação de vídeo apresentando resultado e arquitetura
- Documentação técnica do hardware e testes executados

## Como rodar (simulação)
1. Abra o esquema Wokwi disponível em /hardware.
2. Faça upload dos códigos em /publisher e /subscriber.
3. Siga as instruções de uso em cada subpasta.
4. Para medições de latência, consulte o arquivo em /resultados.

## Documentação extra
- Artigo final em `doc/artigo_final.pdf`
- Vídeo demonstrativo: [link para YouTube]
- Prints de funcionamento/evidências
- Tabela e gráfico dos testes

## Créditos
- Aluna: Verônica Lima de Faria
- Orientação: Prof. Andre Luis de Oliveira
- Universidade Presbiteriana Mackenzie (2025)
