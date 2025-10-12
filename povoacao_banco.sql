-- POPULAÇÃO DA TABELA user_register
INSERT INTO user_register (name, username, email, password, phone, institution, last_login, user_type) VALUES
-- Organizadores
('João Silva', 'joao_organizador', 'joao.organizador@faculdade.edu.br', 'hashed_password_789', '(31) 97777-6666', 'Faculdade Tecnológica', '2024-01-15 09:15:00', 'Organizador'),
('Ana Costa', 'ana_organizadora', 'ana.organizadora@universidade.edu.br', 'hashed_password_101', '(41) 96666-5555', 'Universidade Estadual', '2024-01-13 16:45:00', 'Organizador'),
('Carlos Oliveira', 'carlos_organizador', 'carlos.organizador@colégio.edu.br', 'hashed_password_202', '(51) 95555-4444', 'Colégio Técnico', '2024-01-14 11:20:00', 'Organizador'),

-- Professores
('Maria Silva', 'prof_maria', 'maria.silva@universidade.edu.br', 'hashed_password_123', '(11) 9999-8888', 'Universidade Federal', '2024-01-15 10:30:00', 'Professor'),
('Pedro Santos', 'prof_pedro', 'pedro.santos@instituto.edu.br', 'hashed_password_456', '(21) 98888-7777', 'Instituto Federal', '2024-01-14 14:20:00', 'Professor'),
('Fernanda Oliveira', 'prof_fernanda', 'fernanda.oliveira@faculdade.edu.br', 'hashed_password_303', '(31) 97777-6666', 'Faculdade de Tecnologia', '2024-01-13 15:30:00', 'Professor'),

-- Estudantes
('Lucas Pereira', 'aluno_lucas', 'lucas.pereira@gmail.com', 'hashed_password_505', '(11) 94444-3333', 'Universidade Federal', '2024-01-15 08:00:00', 'Estudante'),
('Julia Rodrigues', 'aluna_julia', 'julia.rodrigues@hotmail.com', 'hashed_password_404', '(21) 93333-2222', 'Instituto de Pesquisas', '2024-01-14 13:10:00', 'Estudante'),
('Rafael Costa', 'aluno_rafael', 'rafael.costa@outlook.com', 'hashed_password_606', '(31) 92222-1111', 'Faculdade de Tecnologia', '2024-01-15 12:45:00', 'Estudante'),
('Camila Souza', 'aluna_camila', 'camila.souza@yahoo.com', 'hashed_password_707', '(41) 91111-0000', 'Universidade Tecnológica', '2024-01-12 17:20:00', 'Estudante'),
('Bruno Alves', 'aluno_bruno', 'bruno.alves@bol.com.br', 'hashed_password_808', '(51) 90000-9999', 'Centro de Ciências', '2024-01-14 10:15:00', 'Estudante'),
('Patricia Lima', 'aluna_patricia', 'patricia.lima@uol.com.br', 'hashed_password_909', '(11) 98888-7777', 'Faculdade de Medicina', '2024-01-13 14:25:00', 'Estudante');

-- POPULAÇÃO DA TABELA event
INSERT INTO event (title, description, location, max_capacity, creator_id, event_type, final_date, initial_date, event_end, event_start) VALUES
-- Palestras
('Palestra: Inteligência Artificial na Educação', 'Discussão sobre aplicações de IA no ambiente educacional', 'Auditório Principal - Bloco A', 150, 1, 'Palestra', '2024-02-15', '2024-02-15', '2024-02-15 18:00:00', '2024-02-15 14:00:00'),
('Palestra: Sustentabilidade e Tecnologia', 'Como a tecnologia pode contribuir para um futuro sustentável', 'Sala de Conferências - Campus Central', 100, 2, 'Palestra', '2024-03-10', '2024-03-10', '2024-03-10 17:30:00', '2024-03-10 15:00:00'),

-- Workshops
('Workshop de Python para Iniciantes', 'Aprenda os fundamentos da programação em Python com projetos práticos', 'Laboratório de Informática - Bloco B', 30, 1, 'Workshop', '2024-02-20', '2024-02-15', '2024-02-20 17:00:00', '2024-02-15 09:00:00'),
('Workshop de Desenvolvimento Web Moderno', 'Técnicas avançadas para desenvolvimento web responsivo', 'Laboratório de Tecnologia - Sala 305', 25, 3, 'Workshop', '2024-04-05', '2024-04-01', '2024-04-05 16:00:00', '2024-04-01 14:00:00'),

-- Seminários
('Seminário de Pesquisa em Computação', 'Apresentação de trabalhos científicos na área de computação', 'Auditório de Pós-Graduação', 80, 2, 'Seminário', '2024-03-25', '2024-03-25', '2024-03-25 20:00:00', '2024-03-25 08:30:00'),
('Seminário de Inovação Tecnológica', 'Discussão sobre tendências e inovações no mercado tech', 'Centro de Inovação', 120, 3, 'Seminário', '2024-05-15', '2024-05-15', '2024-05-15 18:30:00', '2024-05-15 09:00:00'),

-- Cursos
('Curso de Data Science Básico', 'Introdução à ciência de dados com Python e pandas', 'Laboratório de Dados - Bloco C', 20, 1, 'Curso', '2024-04-30', '2024-04-10', '2024-04-30 12:00:00', '2024-04-10 14:00:00'),
('Curso de Gestão de Projetos Ágeis', 'Metodologias ágeis para gestão de projetos de TI', 'Sala de Treinamentos - Andar 4', 35, 2, 'Curso', '2024-06-20', '2024-06-05', '2024-06-20 13:00:00', '2024-06-05 10:00:00'),

-- Congressos
('Congresso Nacional de Tecnologia', 'O maior evento de tecnologia do país com palestrantes internacionais', 'Centro de Convenções Municipal', 500, 1, 'Congresso', '2024-07-25', '2024-07-22', '2024-07-25 18:00:00', '2024-07-22 08:00:00'),
('Congresso de Educação Digital', 'Discussões sobre transformação digital na educação', 'Universidade Federal', 300, 3, 'Congresso', '2024-08-30', '2024-08-28', '2024-08-30 17:00:00', '2024-08-28 09:00:00'),

-- Simpósios
('Simpósio de Machine Learning', 'Apresentações sobre avanços em aprendizado de máquina', 'Instituto de Computação', 60, 2, 'Simpósio', '2024-09-10', '2024-09-10', '2024-09-10 16:00:00', '2024-09-10 08:30:00'),
('Simpósio de Segurança da Informação', 'Debates sobre cibersegurança e proteção de dados', 'Auditório de Segurança', 75, 1, 'Simpósio', '2024-10-05', '2024-10-05', '2024-10-05 17:30:00', '2024-10-05 09:00:00'),

-- Fóruns
('Fórum de Startups Universitárias', 'Espaço para discussão e networking entre empreendedores', 'Espaço Empreendedor - Campus', 90, 3, 'Fórum', '2024-11-15', '2024-11-15', '2024-11-15 19:00:00', '2024-11-15 13:00:00'),
('Fórum de Carreiras em TI', 'Oportunidades e tendências no mercado de tecnologia', 'Hall de Eventos - Prédio Principal', 200, 2, 'Fórum', '2024-12-10', '2024-12-10', '2024-12-10 16:30:00', '2024-12-10 10:00:00'),

-- Mesas Redondas
('Mesa Redonda: Ética na Inteligência Artificial', 'Discussão sobre aspectos éticos no desenvolvimento de IA', 'Sala de Debates - Bloco D', 40, 1, 'Mesa Redonda', '2024-03-08', '2024-03-08', '2024-03-08 15:30:00', '2024-03-08 13:00:00'),
('Mesa Redonda: Futuro da Educação com Tecnologia', 'Painel sobre transformação digital nas instituições de ensino', 'Auditório da Reitoria', 100, 3, 'Mesa Redonda', '2024-04-12', '2024-04-12', '2024-04-12 16:00:00', '2024-04-12 14:00:00');

-- POPULAÇÃO DA TABELA app_eventparticipant
INSERT INTO app_eventparticipant (event_id, user_id, registration_date) VALUES
-- Participações em Palestras
(1, 4, '2024-01-20 10:00:00'), (1, 5, '2024-01-21 11:30:00'), (1, 6, '2024-01-22 14:15:00'),
(1, 7, '2024-01-23 09:45:00'), (1, 8, '2024-01-24 16:20:00'),
(2, 9, '2024-02-05 08:20:00'), (2, 10, '2024-02-06 10:35:00'), (2, 11, '2024-02-07 13:40:00'),

-- Participações em Workshops
(3, 7, '2024-01-25 14:30:00'), (3, 8, '2024-01-26 11:15:00'), (3, 9, '2024-01-27 09:50:00'),
(3, 10, '2024-01-28 16:45:00'), (3, 11, '2024-01-29 13:20:00'),
(4, 4, '2024-03-01 15:10:00'), (4, 5, '2024-03-02 10:25:00'), (4, 6, '2024-03-03 14:40:00'),

-- Participações em Seminários
(5, 8, '2024-02-20 12:30:00'), (5, 9, '2024-02-21 15:45:00'), (5, 10, '2024-02-22 11:10:00'),
(6, 7, '2024-04-10 09:35:00'), (6, 11, '2024-04-11 14:20:00'), (6, 12, '2024-04-12 16:55:00'),

-- Participações em Cursos
(7, 4, '2024-03-15 13:25:00'), (7, 5, '2024-03-16 15:40:00'), (7, 6, '2024-03-17 08:55:00'),
(7, 7, '2024-03-18 11:30:00'),
(8, 8, '2024-05-01 10:15:00'), (8, 9, '2024-05-02 14:50:00'), (8, 10, '2024-05-03 16:25:00'),

-- Participações em Congressos
(9, 4, '2024-06-15 12:20:00'), (9, 5, '2024-06-16 14:35:00'), (9, 6, '2024-06-17 10:45:00'),
(9, 7, '2024-06-18 16:15:00'), (9, 8, '2024-06-19 09:40:00'), (9, 9, '2024-06-20 15:10:00'),
(10, 10, '2024-07-10 11:55:00'), (10, 11, '2024-07-11 13:30:00'), (10, 12, '2024-07-12 17:05:00'),

-- Participações em Simpósios
(11, 4, '2024-08-01 09:30:00'), (11, 6, '2024-08-02 11:20:00'), (11, 8, '2024-08-03 14:50:00'),
(12, 5, '2024-09-01 10:40:00'), (12, 7, '2024-09-02 15:25:00'), (12, 9, '2024-09-03 13:15:00'),

-- Participações em Fóruns
(13, 7, '2024-10-10 08:45:00'), (13, 9, '2024-10-11 12:30:00'), (13, 11, '2024-10-12 16:20:00'),
(14, 8, '2024-11-01 14:10:00'), (14, 10, '2024-11-02 10:55:00'), (14, 12, '2024-11-03 15:35:00'),

-- Participações em Mesas Redondas
(15, 4, '2024-02-25 13:45:00'), (15, 5, '2024-02-26 16:30:00'), (15, 6, '2024-02-27 11:40:00'),
(16, 7, '2024-03-20 09:25:00'), (16, 8, '2024-03-21 14:15:00'), (16, 9, '2024-03-22 17:00:00');

-- POPULAÇÃO DA TABELA certificate
INSERT INTO certificate (issue_date, verification_code, event_id, participant_id) VALUES
-- Certificados para Palestras
('2024-02-15 18:30:00', 'PALESTRA-IA-2024-001', 1, 4),
('2024-02-15 18:30:00', 'PALESTRA-IA-2024-002', 1, 5),
('2024-02-15 18:30:00', 'PALESTRA-IA-2024-003', 1, 6),
('2024-03-10 18:00:00', 'PALESTRA-SUST-2024-001', 2, 9),

-- Certificados para Workshops
('2024-02-20 17:30:00', 'WORKSHOP-PYTHON-2024-001', 3, 7),
('2024-02-20 17:30:00', 'WORKSHOP-PYTHON-2024-002', 3, 8),
('2024-02-20 17:30:00', 'WORKSHOP-PYTHON-2024-003', 3, 9),
('2024-04-05 16:30:00', 'WORKSHOP-WEB-2024-001', 4, 4),

-- Certificados para Seminários
('2024-03-25 20:30:00', 'SEMINARIO-PESQ-2024-001', 5, 8),
('2024-03-25 20:30:00', 'SEMINARIO-PESQ-2024-002', 5, 9),
('2024-05-15 19:00:00', 'SEMINARIO-INOV-2024-001', 6, 7),

-- Certificados para Cursos
('2024-04-30 12:30:00', 'CURSO-DATASCIENCE-2024-001', 7, 4),
('2024-04-30 12:30:00', 'CURSO-DATASCIENCE-2024-002', 7, 5),
('2024-06-20 13:30:00', 'CURSO-AGILE-2024-001', 8, 8),

-- Certificados para Congressos
('2024-07-25 18:30:00', 'CONGRESSO-TECH-2024-001', 9, 4),
('2024-07-25 18:30:00', 'CONGRESSO-TECH-2024-002', 9, 5),
('2024-08-30 17:30:00', 'CONGRESSO-EDUDIG-2024-001', 10, 10);

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