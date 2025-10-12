-- Tabela de Usuários
CREATE TABLE user_register (
    id SERIAL PRIMARY KEY,
    username VARCHAR(100) NOT NULL UNIQUE,
    email VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    phone VARCHAR(20),
    institution VARCHAR(255),
    last_login TIMESTAMP,
    user_type VARCHAR(50) NOT NULL CHECK (user_type IN ('organiizador', 'professor', 'aluno'))
);

-- Tabela de Eventos
CREATE TABLE event (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    location VARCHAR(255),
    max_capacity INTEGER,
    creator_id INTEGER NOT NULL,
    event_type VARCHAR(100),
    final_date DATE,
    initial_date DATE,
    event_end TIMESTAMP,
    event_start TIMESTAMP,
    FOREIGN KEY (creator_id) REFERENCES user_register(id) ON DELETE CASCADE
);

-- Tabela de Participantes em Eventos (Tabela de Junção)
CREATE TABLE app_eventparticipant (
    id SERIAL PRIMARY KEY,
    event_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (event_id) REFERENCES event(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES user_register(id) ON DELETE CASCADE,
    UNIQUE(event_id, user_id) -- Evita duplicatas
);

-- Tabela de Certificados
CREATE TABLE certificate (
    id SERIAL PRIMARY KEY,
    issue_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    verification_code VARCHAR(100) NOT NULL UNIQUE,
    event_id INTEGER NOT NULL,
    participant_id INTEGER NOT NULL,
    FOREIGN KEY (event_id) REFERENCES event(id) ON DELETE CASCADE,
    FOREIGN KEY (participant_id) REFERENCES user_register(id) ON DELETE CASCADE
);