function received_value = receive_data(data_id,bamocar_receive_id,bamocar_send_id)
    try
        canch1;
    catch
        canch1 = canChannel('PEAK-System','PCAN_USBBUS1');
        configBusSpeed(canch1,500000);
    end
    Defaults={"0x00","0x201","0x181"};
    if nargin>=1
        Defaults{1}=data_id;
    end
    if nargin>=2
        Defaults{2}=bamocar_receive_id;
    end
    if nargin>=3
        Defaults{3}=bamocar_send_id;
    end
    data=hex2dec(Defaults{1});
    bmc_rcv_id=hex2dec(Defaults{2});
    bmc_sd_id=hex2dec(Defaults{3});
    ask_data_id=hex2dec("0x3D");

    messageout = canMessage(bmc_rcv_id,false,3);
    
    out_dec=bin2dec(strcat(dec2bin(hex2dec("0x00"),8),dec2bin(data,8),dec2bin(ask_data_id,8)));
    pack(messageout,uint32(out_dec),0,24,'LittleEndian')

    transmit(canch1,messageout);

    received_value=0;
    count=0;
    while received_value==0 && count<10
        count=count+1;
        messagein = receive(canch1,1);
        if messagein.ID==bmc_sd_id && messagein.Data(1)==data
            len=messagein.Length;
            strout="";
            for k=2:len-1
                strout=strcat(dec2bin(messagein.Data(k),8),dec2bin(messagein.Data(k+1),8));
            end
            received_value=bin2dec(strout);
        end
    end
end