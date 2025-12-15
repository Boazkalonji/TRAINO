SELECT

    reservation_paiement_paiement.date_paiement,
    reservation_paiement_paiement.nombre_place_reserve,
    reservation_paiement_paiement.montant_paiement,


    gare_gare_depart.libelle_gare,  
    gare_gare_arrive.libelle_gare,  
    tarification_tarification.designation_tarififcation,
    reservation_paiement_mode_paiement.libelle_mode,
    auth_user.username
    
FROM
    public.reservation_paiement_paiement


INNER JOIN
    public.reservation_paiement_mode_paiement ON reservation_paiement_mode_paiement.id = reservation_paiement_paiement.id_mode_paiement_id


INNER JOIN
    public.tarification_tarification ON tarification_tarification.id = reservation_paiement_paiement.id_tarification_id


INNER JOIN
    public.details_voyage_details_voyage ON details_voyage_details_voyage.id = tarification_tarification.id_details_voyage_id -- *** CORRIGÉ ***


INNER JOIN
    public.gare_gare AS gare_gare_depart ON gare_gare_depart.id = details_voyage_details_voyage.id_gare_depart_id


INNER JOIN
    public.gare_gare AS gare_gare_arrive ON gare_gare_arrive.id = details_voyage_details_voyage.id_gare_arrive_id


INNER JOIN
    public.auth_user ON auth_user.id = reservation_paiement_paiement.id_user_id

WHERE

    reservation_paiement_paiement.date_paiement = CURRENT_DATE 
    AND 
  










    ----------------------------------------------------


SELECT
    T1.date_paiement,
    T1.nombre_place_reserve,
    T1.montant_paiement,
    gare_depart.libelle_gare AS gare_depart,
    gare_arrivee.libelle_gare AS gare_arrivee,
    T3.designation_tarififcation,
    T2.libelle_mode,
    T6.username
FROM
    reservation_paiement_paiement AS T1
INNER JOIN
    reservation_paiement_mode_paiement AS T2 ON T2.id = T1.id_mode_paiement_id
INNER JOIN
    tarification_tarification AS T3 ON T3.id = T1.id_tarification_id
INNER JOIN
    details_voyage_details_voyage AS T4 ON T4.id = T3.id_details_voyage_id
LEFT JOIN
    gare_gare AS gare_depart ON gare_depart.id = T4.id_gare_depart_id
LEFT JOIN
    gare_gare AS gare_arrivee ON gare_arrivee.id = T4.id_gare_arrive_id
INNER JOIN
    auth_user AS T6 ON T6.id = T1.id_user_id
WHERE
   

    T2.libelle_mode = 'cash';






    SELECT COUNT(*)
FROM reservation_paiement_paiement AS T1
INNER JOIN reservation_paiement_mode_paiement AS T2 ON T2.id = T1.id_mode_paiement_id
-- ... (reste des jointures)
WHERE T1.date_paiement IS NOT NULL 
AND T1.date_paiement = CURRENT_DATE 
AND T2.libelle_mode = 'cash';












----------------------------------//*//*************************************



SELECT T1.date_paiement,
	T1.nombre_place_reserve,
	T1.montant_paiement,
	gare_depart.libelle_gare AS gare_depart,
	gare_arrivee.libelle_gare AS gare_arrivee,
	T3.designation_tarififcation,
	T2.libelle_mode,
	T6.username
FROM reservation_paiement_paiement AS T1
	INNER JOIN reservation_paiement_mode_paiement AS T2 ON 
	 T2.id = T1.id_mode_paiement_id 
	INNER JOIN tarification_tarification AS T3 ON 
	 T3.id = T1.id_tarification_id 
	INNER JOIN details_voyage_details_voyage AS T4 ON 
	 T4.id = T3.id_details_voyage_id 
	LEFT JOIN gare_gare AS gare_depart ON 
	 gare_depart.id = T4.id_gare_depart_id 
	LEFT JOIN gare_gare AS gare_arrivee ON 
	 gare_arrivee.id = T4.id_gare_arrive_id 
	INNER JOIN auth_user AS T6 ON 
	 T6.id = T1.id_user_id 
WHERE 
	 
	T1.date_paiement = TO_DATE($P{P_CURRENT_DATE_STRING}, 'DD-MM-YYYY')

    