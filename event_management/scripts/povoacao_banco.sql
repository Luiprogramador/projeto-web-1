-- POPULAÇÃO DA TABELA event (agora com coluna `image` e `professor_id`)
INSERT INTO event (title, description, location, max_capacity, creator_id, event_type, final_date, initial_date, event_end, event_start, image, professor_id, event_finalized) VALUES

-- Palestras
('Palestra: Avanços em Inteligência Artificial', 'Exploração das últimas tendências e pesquisas em IA', 'Auditório Principal - Bloco A', 150, 1, 'Palestra', '2024-02-15', '2024-02-15', '18:00:00', '14:00:00', 'eventos/palestra_ia.jpg', 4, False),
('Palestra: Sustentabilidade e Tecnologia', 'Como a tecnologia pode contribuir para um futuro sustentável', 'Sala de Conferências - Campus Central', 100, 2, 'Palestra', '2024-03-10', '2024-03-10', '17:30:00', '15:00:00', 'eventos/palestra_sustentabilidade.jpg', 3, False),

-- Workshops
('Workshop de Python para Iniciantes', 'Aprenda os fundamentos da programação em Python com projetos práticos', 'Laboratório de Informática - Bloco B', 30, 1, 'Workshop', '2024-02-20', '2024-02-15', '17:00:00', '09:00:00', 'eventos/workshop_python.jpg', 3, False),
('Workshop de Desenvolvimento Web Moderno', 'Técnicas avançadas para desenvolvimento web responsivo', 'Laboratório de Tecnologia - Sala 305', 25, 3, 'Workshop', '2024-04-05', '2024-04-01', '16:00:00', '14:00:00', 'eventos/workshop_web.jpg', 4, False),

-- Seminários
('Seminário de Pesquisa em Computação', 'Apresentação de trabalhos científicos na área de computação', 'Auditório de Pós-Graduação', 80, 2, 'Seminário', '2024-03-25', '2024-03-25', '20:00:00', '08:30:00', 'eventos/seminario_pesquisa.jpg', 3, False), 
('Seminário de Inovação Tecnológica', 'Discussão sobre tendências e inovações no mercado tech', 'Centro de Inovação', 120, 3, 'Seminário', '2024-05-15', '2024-05-15', '18:30:00', '09:00:00', 'eventos/seminario_inovacao.jpg', 4, False),

-- Cursos
('Curso de Data Science Básico', 'Introdução à ciência de dados com Python e pandas', 'Laboratório de Dados - Bloco C', 20, 1, 'Curso', '2024-04-30', '2024-04-10', '12:00:00', '14:00:00', 'eventos/curso_datascience.jpg', 3, False),
('Curso de Gestão de Projetos Ágeis', 'Metodologias ágeis para gestão de projetos de TI', 'Sala de Treinamentos - Andar 4', 35, 2, 'Curso', '2024-06-20', '2024-06-05', '13:00:00', '10:00:00', 'eventos/curso_gestao_agil.jpg', 4, False),

-- Congressos
('Congresso Nacional de Tecnologia', 'O maior evento de tecnologia do país com palestrantes internacionais', 'Centro de Convenções Municipal', 500, 1, 'Congresso', '2024-07-25', '2024-07-22', '18:00:00', '08:00:00', 'eventos/congresso_tech.jpg', 4, False), 
('Congresso de Educação Digital', 'Discussões sobre transformação digital na educação', 'Universidade Federal', 300, 3, 'Congresso', '2024-08-30', '2024-08-28', '17:00:00', '09:00:00', 'eventos/congresso_educacao_digital.jpg', 3, False),

-- Simpósios
('Simpósio de Machine Learning', 'Apresentações sobre avanços em aprendizado de máquina', 'Instituto de Computação', 60, 2, 'Simpósio', '2024-09-10', '2024-09-10', '16:00:00', '08:30:00', 'eventos/simposio_ml.jpg', 4, False),
('Simpósio de Segurança da Informação', 'Debates sobre cibersegurança e proteção de dados', 'Auditório de Segurança', 75, 1, 'Simpósio', '2024-10-05', '2024-10-05', '17:30:00', '09:00:00', 'eventos/simposio_seguranca.jpg', 3, False),

-- Fóruns
('Fórum de Startups Universitárias', 'Espaço para discussão e networking entre empreendedores', 'Espaço Empreendedor - Campus', 90, 3, 'Fórum', '2024-11-15', '2024-11-15', '19:00:00', '13:00:00', 'eventos/forum_startups.jpg', 4, False),
('Fórum de Carreiras em TI', 'Oportunidades e tendências no mercado de tecnologia', 'Hall de Eventos - Prédio Principal', 200, 2, 'Fórum', '2024-12-10', '2024-12-10', '16:30:00', '10:00:00', 'eventos/forum_carreiras.jpg', 3, False),

-- Mesas Redondas
('Mesa Redonda: Ética na Inteligência Artificial', 'Discussão sobre aspectos éticos no desenvolvimento de IA', 'Sala de Debates - Bloco D', 40, 1, 'Mesa Redonda', '2024-03-08', '2024-03-08', '15:30:00', '13:00:00', 'eventos/mesa_redonda_etica_ia.jpg', 4, False),
('Mesa Redonda: Futuro da Educação com Tecnologia', 'Painel sobre transformação digital nas instituições de ensino', 'Auditório da Reitoria', 100, 3, 'Mesa Redonda', '2024-04-12', '2024-04-12', '16:00:00', '14:00:00', 'eventos/mesa_redonda_educacao.jpg', 3, False);

-- POPULAÇÃO DA TABELA app_eventparticipant
INSERT INTO app_eventparticipant (event_id, user_id) VALUES
-- Participações em Palestras
(1, 5),  -- aluno_lucas na Palestra IA
(1, 3),  -- prof_maria na Palestra IA
(1, 4),  -- prof_pedro na Palestra IA
(2, 5),  -- aluno_lucas na Palestra Sustentabilidade
(2, 1),  -- joao_organizador na Palestra Sustentabilidade

-- Participações em Workshops
(3, 5),  -- aluno_lucas no Workshop Python
(3, 3),  -- prof_maria no Workshop Python
(3, 2),  -- ana_organizadora no Workshop Python
(4, 4),  -- prof_pedro no Workshop Web
(4, 1),  -- joao_organizador no Workshop Web

-- Participações em Seminários
(5, 5),  -- aluno_lucas no Seminário Pesquisa
(5, 3),  -- prof_maria no Seminário Pesquisa
(5, 2),  -- ana_organizadora no Seminário Pesquisa
(6, 4),  -- prof_pedro no Seminário Inovação
(6, 1),  -- joao_organizador no Seminário Inovação

-- Participações em Cursos
(7, 5),  -- aluno_lucas no Curso Data Science
(7, 3),  -- prof_maria no Curso Data Science
(7, 4),  -- prof_pedro no Curso Data Science
(8, 1),  -- joao_organizador no Curso Gestão Ágil
(8, 2),  -- ana_organizadora no Curso Gestão Ágil

-- Participações em Congressos
(9, 5),  -- aluno_lucas no Congresso Tecnologia
(9, 3),  -- prof_maria no Congresso Tecnologia
(9, 4),  -- prof_pedro no Congresso Tecnologia
(9, 1),  -- joao_organizador no Congresso Tecnologia
(9, 2),  -- ana_organizadora no Congresso Tecnologia
(10, 5), -- aluno_lucas no Congresso Educação Digital
(10, 3), -- prof_maria no Congresso Educação Digital

-- Participações em Simpósios
(11, 4), -- prof_pedro no Simpósio Machine Learning
(11, 2), -- ana_organizadora no Simpósio Machine Learning
(11, 1), -- joao_organizador no Simpósio Machine Learning
(12, 3), -- prof_maria no Simpósio Segurança
(12, 5), -- aluno_lucas no Simpósio Segurança

-- Participações em Fóruns
(13, 5), -- aluno_lucas no Fórum Startups
(13, 3), -- prof_maria no Fórum Startups
(13, 4), -- prof_pedro no Fórum Startups
(14, 1), -- joao_organizador no Fórum Carreiras
(14, 2), -- ana_organizadora no Fórum Carreiras

-- Participações em Mesas Redondas
(15, 3), -- prof_maria na Mesa Redonda Ética IA
(15, 4), -- prof_pedro na Mesa Redonda Ética IA
(15, 1), -- joao_organizador na Mesa Redonda Ética IA
(16, 2), -- ana_organizadora na Mesa Redonda Educação
(16, 5), -- aluno_lucas na Mesa Redonda Educação
(16, 3); -- prof_maria na Mesa Redonda Educação

-- POPULAÇÃO DA TABELA certificate
INSERT INTO certificate (issue_date, verification_code, event_id, participant_id) VALUES
-- Certificados para Palestras
('2024-02-15 18:30:00', 'PALESTRA-IA-2024-001', 1, 5),  -- aluno_lucas
('2024-02-15 18:30:00', 'PALESTRA-IA-2024-002', 1, 3),  -- prof_maria
('2024-03-10 18:00:00', 'PALESTRA-SUST-2024-001', 2, 1),  -- joao_organizador

-- Certificados para Workshops
('2024-02-20 17:30:00', 'WORKSHOP-PYTHON-2024-001', 3, 5),  -- aluno_lucas
('2024-02-20 17:30:00', 'WORKSHOP-PYTHON-2024-002', 3, 3),  -- prof_maria
('2024-04-05 16:30:00', 'WORKSHOP-WEB-2024-001', 4, 4),  -- prof_pedro

-- Certificados para Seminários
('2024-03-25 20:30:00', 'SEMINARIO-PESQ-2024-001', 5, 5),  -- aluno_lucas
('2024-03-25 20:30:00', 'SEMINARIO-PESQ-2024-002', 5, 2),  -- ana_organizadora
('2024-05-15 19:00:00', 'SEMINARIO-INOV-2024-001', 6, 1),  -- joao_organizador

-- Certificados para Cursos
('2024-04-30 12:30:00', 'CURSO-DATASCIENCE-2024-001', 7, 5),  -- aluno_lucas
('2024-04-30 12:30:00', 'CURSO-DATASCIENCE-2024-002', 7, 3),  -- prof_maria
('2024-06-20 13:30:00', 'CURSO-AGILE-2024-001', 8, 2),  -- ana_organizadora

-- Certificados para Congressos
('2024-07-25 18:30:00', 'CONGRESSO-TECH-2024-001', 9, 5),  -- aluno_lucas
('2024-07-25 18:30:00', 'CONGRESSO-TECH-2024-002', 9, 3),  -- prof_maria
('2024-08-30 17:30:00', 'CONGRESSO-EDUDIG-2024-001', 10, 5); -- aluno_lucas

-- CONSULTAS DE VERIFICAÇÃO
-- Verificar contagem de registros
SELECT 
    'user_register' as tabela, COUNT(*) as total FROM user_register
UNION ALL
SELECT 'event', COUNT(*) FROM event
UNION ALL
SELECT 'app_eventparticipant', COUNT(*) FROM app_eventparticipant
UNION ALL
SELECT 'certificate', COUNT(*) FROM certificate;

-- Verificar distribuição por tipo de usuário
SELECT 
    user_type as tipo_usuario,
    COUNT(*) as quantidade
FROM user_register 
GROUP BY user_type 
ORDER BY quantidade DESC;

-- Verificar eventos por tipo
SELECT 
    event_type as tipo_evento,
    COUNT(*) as quantidade,
    AVG(max_capacity) as capacidade_media
FROM event 
GROUP BY event_type 
ORDER BY quantidade DESC;

-- Verificar participantes por evento (agora incluindo o nome)
SELECT 
    e.title as evento,
    e.event_type as tipo,
    COUNT(ap.user_id) as total_participantes,
    e.max_capacity as capacidade_maxima,
    ROUND((COUNT(ap.user_id) * 100.0 / e.max_capacity), 2) as ocupacao_percentual
FROM event e
LEFT JOIN app_eventparticipant ap ON e.id = ap.event_id
GROUP BY e.id, e.title, e.event_type, e.max_capacity
ORDER BY e.event_type, e.title;

-- Nova consulta: Verificar usuários com seus nomes
SELECT 
    name as nome_completo,
    username,
    email,
    user_type as tipo_usuario,
    institution as instituicao
FROM user_register 
ORDER BY user_type, name;

-- NOVA CONSULTA ADICIONADA: Verificar eventos e seus professores
SELECT 
    e.title as evento,
    u.name as professor_responsavel
FROM event e
JOIN user_register u ON e.professor_id = u.id
ORDER BY e.initial_date;