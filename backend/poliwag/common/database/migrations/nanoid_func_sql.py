from django.db import migrations


forwards_sql = """
CREATE EXTENSION IF NOT EXISTS pgcrypto;

CREATE OR REPLACE FUNCTION gen_nanoid()
RETURNS text AS $$
DECLARE
  id text := '';
  id_size int := 13;
  i int := 0;
  char_pool char(64) := '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ';
  bytes bytea := gen_random_bytes(id_size);
  byte int;
  pos int;
BEGIN
  WHILE i < id_size LOOP
    byte := get_byte(bytes, i);
    pos := (byte & 63) + 1; -- + 1 substr starts at 1
    id := id || substr(char_pool, pos, 1);
    i = i + 1;
  END LOOP;
  RETURN id;
END
$$ LANGUAGE PLPGSQL STABLE;
"""

reverse_sql = """
DROP FUNCTION IF EXISTS gen_nanoid;
"""


class Migration(migrations.Migration):
    dependencies = []

    operations = [migrations.RunSQL(sql=forwards_sql, reverse_sql=reverse_sql)]
