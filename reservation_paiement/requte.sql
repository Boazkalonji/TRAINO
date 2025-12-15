SELECT

    T1.numero_billet,
    T1.montant_paiement,
    T1.nombre_place_reserve,
    T1.date_paiement,
    T1.qr_code, 
    

    T6.username AS nom_client, 

    T2.libelle_mode AS mode_paiement_libelle, 


    T3.designation_tarififcation AS classe_tarif,
    

    T5.heure_depart, 
    
 
    T4.distance AS distance_km,
    

    T7.numero_voiture,
    

    G_DEP.libelle_gare AS gare_depart_libelle, 
    G_ARR.libelle_gare AS gare_arrivee_libelle 

FROM
    reservation_paiement_paiement AS T1
    
INNER JOIN reservation_paiement_mode_paiement AS T2 ON T2.id = T1.id_mode_paiement_id
INNER JOIN tarification_tarification AS T3 ON T3.id = T1.id_tarification_id
INNER JOIN details_voyage_details_voyage AS T4 ON T4.id = T3.id_details_voyage_id
INNER JOIN auth_user AS T6 ON T6.id = T1.id_user_id


INNER JOIN voyage_voyage AS T5 ON T5.id = T4.id_voyage_id


INNER JOIN voiture_voiture AS T7 ON T7.id_tarification_id = T3.id 


INNER JOIN gare_gare AS G_DEP ON G_DEP.id = T4.id_gare_depart_id
INNER JOIN gare_gare AS G_ARR ON G_ARR.id = T4.id_gare_arrive_id 

WHERE
    T1.id_user_id = $P{P_ID_CLIENT} 
    AND T1.statut = TRUE 

ORDER BY
    T1.id DESC 
LIMIT 1;