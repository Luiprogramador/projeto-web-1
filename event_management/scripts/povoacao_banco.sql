-- ==============================================================================
-- 1. POPULAÇÃO DA TABELA event
-- ==============================================================================
-- Regras:
-- - Datas em 2026 (Futuro, já que hoje é Dez/2025).
-- - Criadores: Apenas 1 e 2 (Organizadores).
-- - Professores Responsáveis: Alternando apenas 3 e 4.
-- - Eventos não finalizados (False).

INSERT INTO event (title, description, location, max_capacity, creator_id, event_type, final_date, initial_date, event_end, event_start, image, professor_id, event_finalized) VALUES

-- Palestras
('Palestra: Avanços em Inteligência Artificial', 'Exploração das últimas tendências e pesquisas em IA Generativa e LLMs.', 'Auditório Principal - Bloco A', 150, 1, 'Palestra', '2026-02-15', '2026-02-15', '18:00:00', '14:00:00', 'eventos/palestra_ia.jpg', 6, False),
('Palestra: Sustentabilidade e Green Tech', 'Como a tecnologia pode contribuir para um futuro sustentável.', 'Sala de Conferências - Campus Central', 100, 2, 'Palestra', '2026-03-10', '2026-03-10', '17:30:00', '15:00:00', 'eventos/palestra_sustentabilidade.jpg', 4, False),

-- Workshops
('Workshop de Python para Iniciantes', 'Aprenda os fundamentos da programação em Python 3.12 com projetos práticos.', 'Laboratório de Informática - Bloco B', 30, 1, 'Workshop', '2026-02-20', '2026-02-15', '17:00:00', '09:00:00', 'eventos/workshop_python.jpg', 6, False),
('Workshop de Desenvolvimento Web Moderno', 'Técnicas avançadas com Django, React e Tailwind CSS.', 'Laboratório de Tecnologia - Sala 305', 25, 2, 'Workshop', '2026-04-05', '2026-04-01', '16:00:00', '14:00:00', 'eventos/workshop_web.jpg', 4, False),

-- Seminários
('Seminário de Pesquisa em Computação', 'Apresentação de trabalhos científicos e teses na área de computação quântica.', 'Auditório de Pós-Graduação', 80, 1, 'Seminário', '2026-03-25', '2026-03-25', '20:00:00', '08:30:00', 'eventos/seminario_pesquisa.jpg', 3, False), 
('Seminário de Inovação Tecnológica', 'Discussão sobre tendências e inovações no mercado tech para 2030.', 'Centro de Inovação', 120, 2, 'Seminário', '2026-05-15', '2026-05-15', '18:30:00', '09:00:00', 'eventos/seminario_inovacao.jpg', 4, False),

-- Cursos
('Curso de Data Science Básico', 'Introdução à ciência de dados com Python, Pandas e Matplotlib.', 'Laboratório de Dados - Bloco C', 20, 1, 'Curso', '2026-04-30', '2026-04-10', '12:00:00', '14:00:00', 'eventos/curso_datascience.jpg', 3, False),
('Curso de Gestão de Projetos Ágeis', 'Metodologias ágeis (Scrum e Kanban) para gestão de projetos de TI.', 'Sala de Treinamentos - Andar 4', 35, 2, 'Curso', '2026-06-20', '2026-06-05', '13:00:00', '10:00:00', 'eventos/curso_gestao_agil.jpg', 6, False),

-- Congressos
('Congresso Nacional de Tecnologia', 'O maior evento de tecnologia do país com palestrantes internacionais.', 'Centro de Convenções Municipal', 500, 1, 'Congresso', '2026-07-25', '2026-07-22', '18:00:00', '08:00:00', 'eventos/congresso_tech.jpg', 3, False), 
('Congresso de Educação Digital', 'Discussões sobre transformação digital e IA na educação superior.', 'Universidade Federal', 300, 2, 'Congresso', '2026-08-30', '2026-08-28', '17:00:00', '09:00:00', 'eventos/congresso_educacao_digital.jpg', 4, False),

-- Simpósios
('Simpósio de Machine Learning', 'Apresentações sobre avanços em aprendizado de máquina e redes neurais.', 'Instituto de Computação', 60, 1, 'Simpósio', '2026-09-10', '2026-09-10', '16:00:00', '08:30:00', 'eventos/simposio_ml.jpg', 3, False),
('Simpósio de Segurança da Informação', 'Debates sobre cibersegurança, LGPD e proteção de dados.', 'Auditório de Segurança', 75, 2, 'Simpósio', '2026-10-05', '2026-10-05', '17:30:00', '09:00:00', 'eventos/simposio_seguranca.jpg', 4, False),

-- Fóruns
('Fórum de Startups Universitárias', 'Espaço para discussão, pitch e networking entre empreendedores.', 'Espaço Empreendedor - Campus', 90, 1, 'Fórum', '2026-11-15', '2026-11-15', '19:00:00', '13:00:00', 'eventos/forum_startups.jpg', 3, False),
('Fórum de Carreiras em TI', 'Oportunidades, análise de currículo e tendências no mercado.', 'Hall de Eventos - Prédio Principal', 200, 2, 'Fórum', '2026-12-10', '2026-12-10', '16:30:00', '10:00:00', 'eventos/forum_carreiras.jpg', 6, False),

-- Mesas Redondas
('Mesa Redonda: Ética na Inteligência Artificial', 'Discussão sobre aspectos éticos, viés e regulação da IA.', 'Sala de Debates - Bloco D', 40, 1, 'Mesa Redonda', '2026-03-08', '2026-03-08', '15:30:00', '13:00:00', 'eventos/mesa_redonda_etica_ia.jpg', 3, False),
('Mesa Redonda: Futuro da Educação', 'Painel sobre o impacto da tecnologia nas instituições de ensino.', 'Auditório da Reitoria', 100, 2, 'Mesa Redonda', '2026-04-12', '2026-04-12', '16:00:00', '14:00:00', 'eventos/mesa_redonda_educacao.jpg', 4, False);


-- ==============================================================================
-- 2. POPULAÇÃO DA TABELA app_eventparticipant (INSCRIÇÕES)
-- ==============================================================================
-- Regras:
-- - IDs 1 e 2 (Organizadores) NÃO participam.
-- - IDs 3 e 4 (Professores) participam.
-- - IDs 5 a 11 (Estudantes e Novos Usuários criados pelo Python) participam.

INSERT INTO app_eventparticipant (event_id, user_id) VALUES
-- Evento 1: Palestra IA (Super lotado)
(1, 5), (1, 6), (1, 7), (1, 8), (1, 9), (1, 10), (1, 11), (1, 3), (1, 4),

-- Evento 2: Palestra Sustentabilidade
(2, 5), (2, 7), (2, 11), (2, 6), (2, 4),

-- Evento 3: Workshop Python (Foco em iniciantes - Alunos 5, 7, 8, 9)
(3, 7), (3, 8), (3, 9), (3, 5), (3, 11),

-- Evento 4: Workshop Web (Foco em design/front - Alunos 10, 11)
(4, 7), (4, 11), (4, 10), (4, 5), (4, 4),

-- Evento 5: Seminário Pesquisa (Professores e alunos avançados)
(5, 5), (5, 9), (5, 8), (5, 3), (5, 6),

-- Evento 6: Seminário Inovação
(6, 7), (6, 10), (6, 4), (6, 3), (6, 6),

-- Evento 7: Curso Data Science (Beatriz ID 9 ama isso)
(7, 9), (7, 5), (7, 8), (7, 3),

-- Evento 8: Curso Gestão Ágil
(8, 7), (8, 8), (8, 6), (8, 4),

-- Evento 9: Congresso Tech (Evento grande, quase todos vão)
(9, 5), (9, 7), (9, 8), (9, 9), (9, 10), (9, 11), (9, 3), (9, 4), (9, 6),

-- Evento 10: Congresso Educação Digital
(10, 3), (10, 4), (10, 6), (10, 5), (10, 9),

-- Evento 11: Simpósio ML
(11, 9), (11, 8), (11, 5), (11, 6),

-- Evento 12: Simpósio Segurança
(12, 7), (12, 8), (12, 4), (12, 3),

-- Evento 13: Fórum Startups
(13, 7), (13, 10), (13, 11), (13, 5),

-- Evento 14: Fórum Carreiras
(14, 5), (14, 7), (14, 8), (14, 9), (14, 10), (14, 11),

-- Evento 15: Mesa Ética IA
(15, 3), (15, 4), (15, 6), (15, 9),

-- Evento 16: Mesa Educação
(16, 3), (16, 4), (16, 6), (16, 11);


-- ==============================================================================
-- 3. TABELA DE CERTIFICADOS (COMENTADA)
-- ==============================================================================
-- MOTIVO: Como os eventos foram movidos para 2026 (Futuro), não é possível
-- emitir certificados agora. Na apresentação, use o botão "Finalizar Evento"
-- na interface do Organizador para gerar um certificado ao vivo.

/*
INSERT INTO certificate (issue_date, verification_code, event_id, participant_id) VALUES
('2026-02-15 18:30:00', 'PALESTRA-IA-2024-001', 1, 5);
*/


-- ==============================================================================
-- 4. CONSULTAS ÚTEIS PARA A APRESENTAÇÃO
-- ==============================================================================

-- Verificar distribuição de inscritos
SELECT 
    e.title as Evento, 
    COUNT(ap.user_id) as Inscritos
FROM event e
LEFT JOIN app_eventparticipant ap ON e.id = ap.event_id
GROUP BY e.title;

-- Verificar Professores Responsáveis (Deve ser apenas 3 e 4)
SELECT 
    e.title, 
    e.professor_id 
FROM event e;