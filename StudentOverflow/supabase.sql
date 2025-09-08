
create extension if not exists "uuid-ossp";


create table if not exists public.profiles (
  id uuid primary key references auth.users(id) on delete cascade,
  email text unique not null,
  created_at timestamp with time zone default now()
);


create table if not exists public.questions (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null references public.profiles(id) on delete cascade,
  title text not null,
  body text,
  created_at timestamp with time zone default now()
);


create table if not exists public.answers (
  id uuid primary key default gen_random_uuid(),
  question_id uuid not null references public.questions(id) on delete cascade,
  user_id uuid not null references public.profiles(id) on delete cascade,
  body text not null,
  created_at timestamp with time zone default now()
);


alter table public.profiles enable row level security;
alter table public.questions enable row level security;
alter table public.answers enable row level security;


drop policy if exists "read_profiles" on public.profiles;
create policy "read_profiles" on public.profiles for select using (true);

drop policy if exists "insert_own_profile" on public.profiles;
create policy "insert_own_profile" on public.profiles for insert with check (auth.uid() = id);

drop policy if exists "read_questions" on public.questions;
create policy "read_questions" on public.questions for select using (true);

drop policy if exists "insert_questions" on public.questions;
create policy "insert_questions" on public.questions for insert with check (auth.uid() = user_id);

drop policy if exists "read_answers" on public.answers;
create policy "read_answers" on public.answers for select using (true);

drop policy if exists "insert_answers" on public.answers;
create policy "insert_answers" on public.answers for insert with check (auth.uid() = user_id);


comment on table public.profiles is 'profiles';
comment on table public.questions is 'questions';
comment on table public.answers is 'answers';