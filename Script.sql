select u.id, u.username  from users u
inner join statistic_profiles sp on sp.user_id = u.id
inner join reservations r on r.statistic_profile_id = sp.id



select (s.end_at-s.start_at) as consumo, u.id, u.username, s.start_at, s.end_at, g."name"  from slots s
inner join slots_reservations sr on sr.slot_id = s.id
inner join reservations r on r.id = sr.reservation_id
inner join statistic_profiles sp on r.statistic_profile_id = sp.id
inner join users u on u.id = sp.user_id 
inner join "groups" g on g.id = sp.group_id 
where s.start_at between  '2023-08-10 08:00' and '2023-08-11 22:30' and r.reservable_id between 8 and 10
order by s.end_at desc



select f.id, f.username, f.consumo from (select extract (minute from (s.end_at-s.start_at)) as consumo, u.id, u.username  from slots s
inner join slots_reservations sr on sr.slot_id = s.id
inner join reservations r on r.id = sr.reservation_id
inner join statistic_profiles sp on r.statistic_profile_id = sp.id
inner join users u on u.id = sp.user_id
where s.start_at between  '2023-08-10' and '2023-08-11' and r.reservable_id between 8 and 10) as f, users u
group by f.id, f.username, f.consumo
