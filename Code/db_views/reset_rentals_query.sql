-- to reset the rentals done using the UI, execute below scripts
    
    delete from rental ;
   
    
    update bike_status set is_rented = 0, is_available = 1 ;
    