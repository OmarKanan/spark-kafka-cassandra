create keyspace test with replication = {'class':'SimpleStrategy','replication_factor':1};
create table test.users (email text primary key, otp int);
create table test.valid (email text, ts timestamp, valid boolean, primary key(email, ts));
