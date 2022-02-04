query_sshh ='''
select alias, nombre, sh.servicio_id, sh.id,sh.fecha_creacion,sh.fecha_actualizacion
from servicio_historico sh 
left join servicio s on sh.servicio_id = s.id
left join contrato c on c.id = s.contrato_id
where 
--c.id in (2,3,4,5,6,7,8,10,12,16,17,20,21,23) --Contratos Santiago
--c.id in (24,25,27,29,32,34) --Contratos LSN-CPO
c.id =63--in (2,3,4,5,6,7,8,10,12,16,17,20,21,23,24,25,27,29,32,34,63) --Contratos Serena y Stgo y CPO
'''

query_viajes = '''
select sh.alias,
s.id as servicio_id,
v.servicio_historico_id,
v.id as contador_viajes,
v.viaje_id,
cast(v.fecha_inicio as TIMESTAMP) as fecha_inicio1,
v.fecha_inicio,
cast(v.fecha_termino AT TIME ZONE uzh.region as timestamp) as fecha_termino,
uzh.region,
v.estado,
v.eliminado,
v.movil_id,
m.numero_interno,
sh.dias_semana,
s.contrato_id,
c.nombre,
cc.id_contrato_softland,
v.km_inicial_can,
v.km_final_can,
v.distancia_can,
v.km_inicial_gps,
v.km_final_gps,
v.distancia_gps,
cast(DATE_TRUNC('second', v.fecha_inicio_gps + '00:00:00.5') AT TIME ZONE uzh.region as timestamp) as fecha_inicio_gps,
cast(DATE_TRUNC('second', v.fecha_inicio_administrador + '00:00:00.5') AT TIME ZONE uzh.region as timestamp) as fecha_inicio_administrador,
cast(DATE_TRUNC('second', v.fecha_inicio_conductor + '00:00:00.5') AT TIME ZONE uzh.region as timestamp) as fecha_inicio_conductor,
cast(DATE_TRUNC('second', v.fecha_termino_gps + '00:00:00.5') AT TIME ZONE uzh.region as timestamp) as fecha_termino_gps,
cast(DATE_TRUNC('second', v.fecha_termino_administrador + '00:00:00.5') AT TIME ZONE uzh.region as timestamp) as fecha_termino_administrador,
cast(DATE_TRUNC('second', v.fecha_termino_conductor + '00:00:00.5') AT TIME ZONE uzh.region as timestamp) as fecha_termino_conductor,
v.fecha_inicio_real,
v.fecha_termino_real,
case 
	when v.distancia_can is null then v.distancia_gps/1000
	else distancia_can
end distancia,
case
	when distancia_can is null and distancia_gps is null then null
	when distancia_can is null then 'GPS'
	else 'CAN'
end dispositivo
from viaje v
left join servicio_historico sh on v.servicio_historico_id = sh.id
left join ubicacion_zona_horaria uzh on sh.ubicacion_zona_horaria_inicio_id = uzh.id
left join servicio s on sh.servicio_id = s.id
left join contrato c on c.id = s.contrato_id
left join contrato_corporativo cc on c.id = cc.contrato_id
left join movil m on m.id = v.movil_id 
where 
--c.id in (2,3,4,5,6,7,8,10,12,16,17,20,21,23) --Contratos Santiago
c.id in (2,3,4,5,6,7,8,10,12,16,17,20,21,22,23,24,25,27,29,32,34,60,63) --Contratos LSN-CPO
/*
2: C SCL ANGLOAMERICAN EL SOLDADO
3: C SCL ANGLOAMERICAN CHAGRES
4: C SCL ANGLOAMERICAN LAS TORTOLAS
5: C SCL ANGLOAMERICAN LOS BRONCES
6: C SCL ANGLOAMERICAN GPRO
7: C SCL BREDEN MASTER
8: C SCL SODIMAC
9: C SCL ANGLOAMERICAN EL SOLDADO - ARRIGONI (?)
10: C SCL CMPC
11: S CCP ENAP EMALCO (?)
12: C SCL GOOD YEAR
13 NO EXISTE
14: C SCL MAQSA (NO VIGENTE)
15 NO EXISTE
16: C SCL SODEXO NESTLE
17: C SCL SODEXO CD QUILICURA
18: TRAFICO SANTIAGO (?)
19: SPOT LOCAL (?)
20: C SCL ENAEX EL SOLDADO
21: C SCL COMPASS EL SOLDADO
22: C SCL ENAP ACONCAGUA
23: C SCL PUERTO CENTRAL
63: C SCL ENAP MAIPU (EMALCO)

24: C LSN AURA
25: C CPO ATACAMA KOZAN
26: C CPO ENAMI
27: C CPO EVH CANDELARIA
28: C CPO FINNING
29: C CPO GEOVITA
30: C LSN ORIZON
32: C CPO MINERA CANDELARIA
33: C CPO EICSA SERV. ATACAMA
34: C CPO IM SPA
35: C CPO PUCOBRE
59: C CPO SCM FRANKE
60: C CPO ENAEX FRANKE
216: C CPO COMPASS CANDELARIA
212: C CPO COMPASS FRA
c.id in (24,25,26,27,28,29,30,32,33,34,35)
*/
and v.fecha_inicio > '2021-08-01 00:00:00' and v.fecha_inicio < now()
and (v.estado = 'FINALIZADO' or v.estado = 'NO_INICIADO' or v.estado = 'ANULADO')
--group by numero_interno,v.distancia_can,v.distancia_gps,s.contrato_id,c.nombre
--and substring(alias,1,12) = 'AA LB_S_VOTA'
--order by fecha_inicio desc
'''