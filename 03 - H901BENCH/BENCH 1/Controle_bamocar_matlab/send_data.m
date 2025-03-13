function send_data(data_id,value,dlc,bamocar_receive_id)
    canch1 = canChannel('PEAK-System','PCAN_USBBUS1');
    configBusSpeed(canch1,500000);
    start(canch1)

    Defaults={"0x00",0,3,"0x201"};
    if nargin>=1
        Defaults{1}=data_id;
    end
    if nargin>=2
        if isa(value,"string")
            Defaults{2}=hex2dec(value);
        else
            Defaults{2}=value;
        end
    end
    if nargin>=3
        Defaults{3}=dlc;
    end
    if nargin>=4
        Defaults{4}=bamocar_receive_id;
    end
    data=hex2dec(Defaults{1});
    val=Defaults{2};
    bmc_rcv_id=hex2dec(Defaults{4});
    valbin=dec2bin(val,8);
    dlc_f=Defaults{3};
    dlc_r=floor(length(valbin)/8);
    messageout = canMessage(bmc_rcv_id,false,dlc_f);
    
    strout=dec2bin(data,8);
    for k=0:dlc_r-1
        strout=strcat(valbin(k*8+1:(k+1)*8),strout);
    end
    for k=dlc_r:dlc_f-2
        strout=strcat("00000000",strout);
    end
    out_dec=bin2dec(strout);

    pack(messageout,uint64(out_dec),0,dlc_f*8,'LittleEndian');
    transmit(canch1,messageout);
    stop(canch1)
end