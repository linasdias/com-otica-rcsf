'use client';

import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { X } from 'lucide-react';
import React, { useCallback, useEffect, useState } from 'react';

export default function BinaryTransmitter() {
  const [message, setMessage] = useState('');
  const [isTransmitting, setIsTransmitting] = useState(false);
  const [countdown, setCountdown] = useState(3);
  const [currentBit, setCurrentBit] = useState('');
  const [transmissionStatus, setTransmissionStatus] = useState('idle');
  const [transmitInterval, setTransmitInterval] = useState<NodeJS.Timeout | null>(null);

  // Sequência de sincronização de bits
  const syncSequence = ['1', '0', '0', '1'];

  // Concatena a sequência de sincronização ao início da mensagem
  const fullMessage = syncSequence.join('') + message;

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const value = e.target.value;
    if (/^[01]*$/.test(value)) {
      setMessage(value);
    }
  };

  const handleSubmit = useCallback((e: React.FormEvent) => {
    e.preventDefault();
    setIsTransmitting(true);
    setCountdown(3);
    setTransmissionStatus('idle');
  }, [message]);

  const stopTransmission = () => {
    setIsTransmitting(false);
    setCurrentBit('');
    setMessage('');
    setCountdown(3);
    setTransmissionStatus('idle');
    if (transmitInterval) {
      clearInterval(transmitInterval);
    }
  };

  useEffect(() => {
    if (isTransmitting && countdown > 0) {
      const timer = setTimeout(() => setCountdown(countdown - 1), 1000);
      return () => clearTimeout(timer);
    }
    if (countdown === 0 && fullMessage) {
      setTransmissionStatus('start');
      let index = -1;
      const transmit = setInterval(() => {
        if (index === -1) {
          setTransmissionStatus('transmitting');
          index++;
        } else if (index < fullMessage.length) {
          setCurrentBit(fullMessage[index]);
          index++;
        } else {
          setTransmissionStatus('end');
          clearInterval(transmit);
          setTimeout(() => {
            stopTransmission();
          }, 1000);
        }
      }, 1000);
      setTransmitInterval(transmit);
      return () => clearInterval(transmit);
    }
  }, [isTransmitting, countdown, fullMessage]);

  const getTransmissionColor = () => {
    switch (transmissionStatus) {
      case 'start':
        return 'bg-[#00C800]'; // Vermelho para início
      case 'transmitting':
        return currentBit === '1' ? 'bg-[#ffffff]' : 'bg-[#000000]'; // Branco para 1 e Preto para 0
      case 'end':
        return 'bg-[#C80000]'; // Verde para fim
      default:
        return 'bg-[#111827]'; // Cinza escuro
    }
  };

  return (
    <div className={`min-h-screen flex flex-col items-center justify-center p-4 transition-colors duration-300 ${isTransmitting ? getTransmissionColor() : 'bg-gray-900'}`}>
      {isTransmitting && (
        <button
          onClick={stopTransmission}
          className="absolute top-4 right-4 text-white bg-red-600 rounded-full p-2 hover:bg-red-700 transition"
          aria-label="Stop Transmission"
        >
          <X size={20} />
        </button>
      )}
      {!isTransmitting ? (
        <div className="w-full max-w-md bg-gray-800 rounded-lg shadow-md p-6">
          <h1 className="text-2xl font-bold mb-4 text-center text-white">Binary Message Transmitter</h1>
          <form onSubmit={handleSubmit} className="mb-4">
            <Input
              type="text"
              value={message}
              onChange={handleInputChange}
              placeholder="Enter binary message"
              className="w-full mb-2 text-lg bg-gray-700 text-white placeholder-gray-400"
            />
            <Button type="submit" className="w-full text-lg" disabled={!message}>
              Transmit
            </Button>
          </form>
        </div>
      ) : (
        <div className="text-center">
          {countdown > 0 ? (
            <>
              <div className="text-6xl font-bold mb-4 text-white">{countdown}</div>
              <p className="text-xl font-semibold mb-4 text-white">
                Aponte o dispositivo para a câmera enquanto o temporizador estiver na tela
              </p>
            </>
          ) : (
            <div className="text-6xl font-bold text-[#808080]">
              {transmissionStatus === 'transmitting' ? currentBit : ''}
            </div>
          )}
        </div>
      )}
    </div>
  );
}
