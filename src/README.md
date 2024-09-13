# Intro
Основное приложение

# DB
## Базовые фичи
INSERT INTO public.features (id, enabled, "name", "type") VALUES(6, true, 'telegram notificaitons', 'notification');
INSERT INTO public.features (id, enabled, "name", "type") VALUES(9, true, '24 hour dynamic', 'statis');
INSERT INTO public.features (id, enabled, "name", "type") VALUES(10, true, 'Toxic messages 24 hour dynamic', 'statis');
INSERT INTO public.features (id, enabled, "name", "type") VALUES(3, true, 'Block toxic requests from client', 'binary_filter');
INSERT INTO public.features (id, enabled, "name", "type") VALUES(13, true, 'Determine a request subject', 'multi_filter');
INSERT INTO public.features (id, enabled, "name", "type") VALUES(14, true, 'Block toxic answers from AI', 'multi_filter');
INSERT INTO public.features (id, enabled, "name", "type") VALUES(16, true, 'Apply filters without blocking.', 'filter_mode');
INSERT INTO public.features (id, enabled, "name", "type") VALUES(15, true, 'Determine a llm answer subject', 'binary_filter');