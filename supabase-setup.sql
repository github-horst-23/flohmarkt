-- Einmal im SQL Editor deines Supabase-Projekts ausführen.
create table public.fitness_data (
  user_id uuid primary key references auth.users (id) on delete cascade,
  payload jsonb not null,
  version bigint not null default 1,
  updated_at timestamptz not null default now()
);

alter table public.fitness_data enable row level security;
revoke all on table public.fitness_data from anon, authenticated;
grant select, insert, update on table public.fitness_data to authenticated;

create policy "Users can read their own fitness data"
  on public.fitness_data for select to authenticated
  using (auth.uid() = user_id);

create policy "Users can create their own fitness data"
  on public.fitness_data for insert to authenticated
  with check (auth.uid() = user_id);

create policy "Users can update their own fitness data"
  on public.fitness_data for update to authenticated
  using (auth.uid() = user_id)
  with check (auth.uid() = user_id);
