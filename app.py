import time
from flask import Flask, render_template, request, redirect, url_for
from prometheus_client import generate_latest, CollectorRegistry, Counter, Gauge
import redis
import os

app = Flask(__name__)

# Obtendo o host e a porta do Redis do ambiente do Kubernetes
redis_host = os.environ.get('REDIS_HOST', 'redis-service')
redis_port = os.environ.get('REDIS_PORT', '6379')

# Criando uma conexão com o Redis
r = redis.Redis(host=redis_host, port=int(redis_port), db=0)

# Definindo as fotos
fotos = {
    'foto1': 'URL_FOTO_1',
    'foto2': 'URL_FOTO_2',
    'foto3': 'URL_FOTO_3',
    'foto4': 'URL_FOTO_4',
    'foto5': 'URL_FOTO_5',
    'foto6': 'URL_FOTO_6'
}

# Definindo as métricas
registry = CollectorRegistry()
requests_counter = Counter('my_app_requests_total', 'Número total de solicitações recebidas', registry=registry)
memory_usage = Gauge('my_app_memory_usage', 'Uso de memória da aplicação', registry=registry)
request_latency = Gauge('my_app_request_latency_seconds', 'Latência das solicitações', registry=registry)
response_time_summary = Gauge('my_app_response_time_seconds', 'Resumo do tempo de resposta', registry=registry)
exception_counter = Counter('my_app_exceptions_total', 'Número total de exceções', registry=registry)

# Métricas adicionais
successful_votes_counter = Counter('my_app_successful_votes_total', 'Número total de votos bem-sucedidos', registry=registry)
failed_votes_counter = Counter('my_app_failed_votes_total', 'Número total de votos falhos', registry=registry)
photo_votes_gauge = Gauge('my_app_photo_votes', 'Número de votos por foto', ['photo'], registry=registry)
active_users_gauge = Gauge('my_app_active_users', 'Número de usuários ativos', registry=registry)
average_processing_time_gauge = Gauge('my_app_average_processing_time_seconds', 'Tempo médio de processamento', registry=registry)

# Rota principal para exibir a página
@app.route('/')
def index():
    return render_template('index.html', fotos=fotos)

# Rota para registrar um voto
@app.route('/votar', methods=['POST'])
def votar():
    foto_vencedora = request.form['foto_vencedora']
    foto_perdedora = request.form['foto_perdedora']
    
    ip_address = request.remote_addr  # Obtém o endereço IP do cliente
    
    # Verifica se o endereço IP já votou
    if r.get(ip_address):
        time.sleep(3)  # Delay de 3 segundos
        return redirect(url_for('index'))
        
    r.set(ip_address, 1)  # Registra o endereço IP no Redis
    r.incr(foto_vencedora)
    r.incr(foto_perdedora)
    
    successful_votes_counter.inc()  # Incrementa o contador de votos bem-sucedidos
    time.sleep(3)  # Delay de 3 segundos
    
    # Simula um voto falho (para fins de demonstração)
    if foto_vencedora == foto_perdedora:
        failed_votes_counter.inc()  # Incrementa o contador de votos falhos
    
    return redirect(url_for('index'))

# ...

# Rota para obter o ranking
@app.route('/ranking')
def obter_ranking():
    ranking = []
    for foto in fotos:
        votos = r.get(foto)
        if votos is None:
            votos = 0
        else:
            votos = int(votos)
        ranking.append((foto, votos))
    
    ranking = sorted(ranking, key=lambda x: x[1], reverse=True)
    return ranking

# Rota para expor as métricas
@app.route('/metrics')
def metrics():
    # Atualiza as métricas
    requests_counter.inc()
    memory_usage.set(512)
    request_latency.set(0.5)
    response_time_summary.set(0.2)
    exception_counter.inc()
    
    # Métricas adicionais
    active_users_gauge.set(10)
    average_processing_time_gauge.set(0.15)
    
    for foto in fotos:
        votos = r.get(foto)
        if votos is None:
            votos = 0
        else:
            votos = int(votos)
        photo_votes_gauge.labels(foto).set(votos)

    # Gera as métricas no formato de exposição do Prometheus usando o registro
    return generate_latest(registry)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
